
import io
import frappe
import base64
import os
import jwt
from pyqrcode import create as qrcreate
from frappe.integrations.utils import make_request
from frappe.utils.data import time_diff_in_seconds
from frappe.utils.password import get_decrypted_password
from frappe.utils.data import add_to_date
from india_compliance.gst_india.utils import load_doc
from india_compliance.gst_india.utils.e_invoice import EInvoiceData
from india_compliance.gst_india.utils.e_invoice import log_e_invoice
from india_compliance.gst_india.api_classes.e_invoice import EInvoiceAPI
import json

from frappe.utils import now_datetime
from urllib.parse import urlencode, urljoin
from india_compliance.gst_india.utils.e_waybill import (
    log_and_process_e_waybill_generation,
)
from india_compliance.gst_india.utils import parse_datetime, send_updated_doc

def einvoice_setup(self, doc=None, *, company_gstin=None):
	self.BASE_PATH = "enriched/ei/api"
	if not self.settings.enable_e_invoice:
		frappe.throw(_("Please enable e-Waybill features in GST Settings first"))
	self.gst_settings = frappe.get_cached_doc("GST Settings")
	if doc:
		company_gstin = doc.company_gstin
		self.default_log_values.update(
			reference_doctype=doc.doctype,
			reference_name=doc.name,
		)

	if self.sandbox_mode:
		company_gstin = "05AAACG2115R1ZN"
		self.username = "05AAACG2115R1ZN"
		self.password = "abc123@@"

	elif not company_gstin:
		frappe.throw(_("Company GSTIN is required to use the e-Waybill API"))

	else:
		self.fetch_credentials(company_gstin, "e-Waybill / e-Invoice")

	self.default_headers.update(
		{
			"authorization": get_auth_token(self),
			"gstin": company_gstin,
			"user_name": self.username,
			"password": self.password,
			"requestid": str(base64.b64encode(os.urandom(18))),
		}
	)

def get_auth_token(self):
	if time_diff_in_seconds(self.gst_settings.token_expiry, now_datetime()) < 150.0 or not self.gst_settings.auth_token:
		fetch_auth_token(self)

	return self.gst_settings.auth_token

def fetch_auth_token(self):
	client_id, client_secret = get_client_details(self)
	headers = {"gspappid": client_id, "gspappsecret": client_secret}
	res = {}
	url = "https://gsp.adaequare.com/gsp/authenticate?grant_type=token"\

	res = make_request("post", url, headers = headers)
	self.gst_settings.auth_token = "{} {}".format(
		res.get("token_type"), res.get("access_token")
	)

	self.gst_settings.token_expiry = add_to_date(None, seconds=res.get("expires_in"))
	self.gst_settings.save(ignore_permissions=True)
	self.gst_settings.reload()
	
def get_client_details(self):
	if self.gst_settings.get('client_id') and self.gst_settings.get('client_secret'):
		return get_decrypted_password("GST Settings", "GST Settings", fieldname = "client_id"), get_decrypted_password("GST Settings", "GST Settings", fieldname = "client_secret")

	return frappe.conf.einvoice_client_id, frappe.conf.einvoice_client_secret

def ewaybill_setup(self, doc=None, *, company_gstin=None):
	self.gst_settings = frappe.get_cached_doc("GST Settings")
	self.BASE_PATH = "enriched/ewb/ewayapi"
	if not self.settings.enable_e_waybill:
		frappe.throw(_("Please enable e-Waybill features in GST Settings first"))

	if doc:
		company_gstin = doc.company_gstin
		self.default_log_values.update(
			reference_doctype=doc.doctype,
			reference_name=doc.name,
		)

	if self.sandbox_mode:
		company_gstin = "05AAACG2115R1ZN"
		self.username = "05AAACG2115R1ZN"
		self.password = "abc123@@"

	elif not company_gstin:
		frappe.throw(_("Company GSTIN is required to use the e-Waybill API"))

	else:
		self.fetch_credentials(company_gstin, "e-Waybill / e-Invoice")

	self.default_headers.update(
		{
			"authorization": get_auth_token(self),
			"gstin": company_gstin,
			"username": self.username,
			"password": self.password,
			"requestid": str(base64.b64encode(os.urandom(18))),
		}
	)

def get_url(self, *parts):
	self.base_url = "https://gsp.adaequare.com"
	if parts and not list(parts)[-1]:
		parts = list(parts)[:-1]
	elif not parts:
		parts = []
	else:
		parts = list(parts)
	if self.BASE_PATH:
		parts.insert(0, self.BASE_PATH)

	if self.sandbox_mode:
		parts.insert(0, "test")

	return urljoin(self.base_url, "/".join(part.strip("/") for part in parts))

def get_gstin_info(self, gstin):
	self.BASE_PATH = "enriched/commonapi"
	self.gst_settings = frappe.get_cached_doc("GST Settings")
	self.default_headers = {
			"authorization": get_auth_token(self),
			"requestid": str(base64.b64encode(os.urandom(18))),
		}
	return self.get("search", params={"action": "TP", "gstin": gstin})

@frappe.whitelist()
def custom_generate_e_invoice(docname, throw=True):
    doc = load_doc("Sales Invoice", docname, "submit")
    try:
        data = EInvoiceData(doc).get_data()
        api = EInvoiceAPI(doc)
        result = api.generate_irn(data)

        # Handle Duplicate IRN
        if result.InfCd == "DUPIRN":
            response = api.get_e_invoice_by_irn(result.Desc.Irn)

            # Handle error 2283:
            # IRN details cannot be provided as it is generated more than 2 days ago
            result = result.Desc if response.error_code == "2283" else response

    except frappe.ValidationError as e:
        if throw:
            raise e

        frappe.clear_last_message()
        frappe.msgprint(
            _(
                "e-Invoice auto-generation failed with error:<br>{0}<br><br>"
                "Please rectify this issue and generate e-Invoice manually."
            ).format(str(e)),
            _("Warning"),
            indicator="yellow",
        )
        return

    doc.db_set(
        {
            "irn": result.Irn,
            "einvoice_status": "Generated",
            "signed_qr_code": result.SignedQRCode #finbyz changes
        }
    )

    invoice_data = None
    if result.SignedInvoice:
        decoded_invoice = json.loads(
            jwt.decode(result.SignedInvoice, options={"verify_signature": False})[
                "data"
            ]
        )
        invoice_data = frappe.as_json(decoded_invoice, indent=4)

    log_e_invoice(
        doc,
        {
            "irn": doc.irn,
            "sales_invoice": docname,
            "acknowledgement_number": result.AckNo,
            "acknowledged_on": parse_datetime(result.AckDt),
            "signed_invoice": result.SignedInvoice,
            "signed_qr_code": result.SignedQRCode,
            "invoice_data": invoice_data,
        },
    )
    #finbyz changes
    is_qrcode_file_attached = doc.qrcode_image and frappe.db.exists(
        "File",
        {
            "attached_to_doctype": doc.doctype,
            "attached_to_name": doc.name,
            "file_url": doc.qrcode_image,
            "attached_to_field": "qrcode_image",
        },
    )

    if not is_qrcode_file_attached:
        if doc.signed_qr_code:
            attach_qrcode_image(doc)
    #finbyz changes end
    if result.EwbNo:
        log_and_process_e_waybill_generation(doc, result, with_irn=True)

    if not frappe.request:
        return

    frappe.msgprint(
        _("e-Invoice generated successfully"),
        indicator="green",
        alert=True,
    )

    return send_updated_doc(doc)

def attach_qrcode_image(doc):
    qrcode = doc.signed_qr_code
    qr_image = io.BytesIO()
    url = qrcreate(qrcode, error="L")
    url.png(qr_image, scale=2, quiet_zone=1)
    qrcode_file = create_qr_code_file(doc, qr_image.getvalue())
    doc.db_set({
        "qrcode_image" : qrcode_file.file_url
    })

def create_qr_code_file(doc, qr_image):
    doctype = doc.doctype
    docname = doc.name
    filename = "QRCode_{}.png".format(docname).replace(os.path.sep, "__")

    _file = frappe.get_doc(
        {
            "doctype": "File",
            "file_name": filename,
            "attached_to_doctype": doctype,
            "attached_to_name": docname,
            "attached_to_field": "qrcode_image",
            "is_private": 0,
            "content": qr_image,
        }
    )
    _file.save()
    frappe.db.commit()
    return _file