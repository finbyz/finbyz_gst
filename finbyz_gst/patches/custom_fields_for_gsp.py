import frappe


def execute():
    create_custom_field_for_einvoice()

def create_custom_field_for_einvoice():

    if not frappe.db.exists("Custom Field", "GST Settings-auth_token"):
        doc = frappe.new_doc("Custom Field")
        doc.dt = "GST Settings"
        doc.label = "Auth Token"
        doc.fieldname = "auth_token"
        doc.insert_after = "api_secret"
        doc.fieldtype = "Data"
        doc.hidden = 1
        doc.save(ignore_permissions=True)
    
    if not frappe.db.exists("Custom Field", "GST Settings-token_expiry"):
        doc = frappe.new_doc("Custom Field")
        doc.dt = "GST Settings"
        doc.label = "Token Expiry"
        doc.fieldname = "token_expiry"
        doc.insert_after = "auth_token"
        doc.fieldtype = "Datetime"
        doc.hidden = 1
        doc.save(ignore_permissions=True)

    if not frappe.db.exists("Custom Field", "GST Settings-client_id"):
        doc = frappe.new_doc("Custom Field")
        doc.dt = "GST Settings"
        doc.label = "Client Id"
        doc.fieldname = "client_id"
        doc.insert_after = "token_expiry"
        doc.fieldtype = "Password"
        doc.save(ignore_permissions=True)
    
    if not frappe.db.exists("Custom Field", "GST Settings-client_secret"):
        doc = frappe.new_doc("Custom Field")
        doc.dt = "GST Settings"
        doc.label = "Client Secret"
        doc.fieldname = "client_secret"
        doc.insert_after = "client_id"
        doc.fieldtype = "Password"
        doc.save(ignore_permissions=True)
    
    if not frappe.db.exists("Custom Field", "Sales Invoice-qrcode_image"):
        doc = frappe.new_doc("Custom Field")
        doc.dt = "Sales Invoice"
        doc.label = "QRCode Image"
        doc.fieldname = "qrcode_image"
        doc.fieldtype = "Code"
        doc.options = "JSON"
        doc.read_only == 1
        doc.hidden==1
        doc.no_copy == 1
        doc.allow_on_submit == 1
        doc.save(ignore_permissions=True)
    
    if not frappe.db.exists("Custom Field", "Sales Invoice-irn_cancel_date"):
        doc = frappe.new_doc("Custom Field")
        doc.dt = "Sales Invoice"
        doc.label = "Cancel Date"
        doc.fieldname = "irn_cancel_date"
        doc.insert_after = "ack_date"
        doc.fieldtype = "Data"
        doc.hidden = 1
        doc.read_only = 1
        doc.no_copy == 1
        doc.print_hide = 1
        doc.save(ignore_permissions=True)

    if not frappe.db.exists("Custom Field", "Sales Invoice-signed_einvoice"):
        doc = frappe.new_doc("Custom Field")
        doc.dt = "Sales Invoice"
        doc.label = "Signed E Invoice"
        doc.fieldname = "signed_einvoice"
        doc.insert_after = "Eway Bill Cancelled"
        doc.fieldtype = "Code"
        doc.options = "JSON"
        doc.hidden = 1
        doc.read_only = 1
        doc.no_copy == 1
        doc.print_hide = 1
        doc.save(ignore_permissions=True)
    
    if not frappe.db.exists("Custom Field", "Sales Invoice-eway_bill_cancelled"):
        doc = frappe.new_doc("Custom Field")
        doc.dt = "Sales Invoice"
        doc.label = "Eway Bill Cancelled"
        doc.fieldname = "eway_bill_cancelled"
        doc.insert_after = "Cancel Date"
        doc.fieldtype = "Check"
        doc.read_only = 1
        doc.no_copy == 1
        doc.print_hide = 1
        doc.depends_on = "eval:(doc.eway_bill_cancelled === 1)"
        doc.save(ignore_permissions=True)
    
    if not frappe.db.exists("Custom Field", "Sales Invoice-signed_qr_code"):
        doc = frappe.new_doc("Custom Field")
        doc.dt = "Sales Invoice"
        doc.label = "Signed QRCode"
        doc.fieldname = "signed_qr_code"
        doc.insert_after = "Signed E Invoice"
        doc.fieldtype = "Code"
        doc.options = "JSON"
        doc.hidden = 1
        doc.read_only = 1
        doc.no_copy == 1
        doc.print_hide = 1
        doc.save(ignore_permissions=True)
    
    if not frappe.db.exists("Custom Field", "Sales Invoice-ack_date"):
        doc = frappe.new_doc("Custom Field")
        doc.dt = "Sales Invoice"
        doc.label = "ack_date"
        doc.fieldname = "ack_date"
        doc.insert_after = "ack_no"
        doc.fieldtype = "Data"
        doc.hidden = 1
        doc.read_only = 1
        doc.no_copy == 1
        doc.print_hide = 1
        doc.save(ignore_permissions=True)
    
    if not frappe.db.exists("Custom Field", "Sales Invoice-ack_no"):
        doc = frappe.new_doc("Custom Field")
        doc.dt = "Sales Invoice"
        doc.label = "ack_no"
        doc.fieldname = "ack_no"
        doc.insert_after = "e-Waybill No."
        doc.fieldtype = "Data"
        doc.hidden = 1
        doc.read_only = 1
        doc.no_copy == 1
        doc.print_hide = 1
        doc.save(ignore_permissions=True)