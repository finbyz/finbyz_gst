from . import __version__ as app_version

app_name = "finbyz_gst"
app_title = "Finbyz GST"
app_publisher = "Finbyz Tech Pvt. Ltd."
app_description = "Custom App for GSP Einvoice API"
app_email = "info@finbyz.tech"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/finbyz_gst/css/finbyz_gst.css"
# app_include_js = "/assets/finbyz_gst/js/finbyz_gst.js"

# include js, css files in header of web template
# web_include_css = "/assets/finbyz_gst/css/finbyz_gst.css"
# web_include_js = "/assets/finbyz_gst/js/finbyz_gst.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "finbyz_gst/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
#	"methods": "finbyz_gst.utils.jinja_methods",
#	"filters": "finbyz_gst.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "finbyz_gst.install.before_install"
# after_install = "finbyz_gst.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "finbyz_gst.uninstall.before_uninstall"
# after_uninstall = "finbyz_gst.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "finbyz_gst.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
#	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
#	"*": {
#		"on_update": "method",
#		"on_cancel": "method",
#		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
#	"all": [
#		"finbyz_gst.tasks.all"
#	],
#	"daily": [
#		"finbyz_gst.tasks.daily"
#	],
#	"hourly": [
#		"finbyz_gst.tasks.hourly"
#	],
#	"weekly": [
#		"finbyz_gst.tasks.weekly"
#	],
#	"monthly": [
#		"finbyz_gst.tasks.monthly"
#	],
# }

# Testing
# -------

# before_tests = "finbyz_gst.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "finbyz_gst.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task": "finbyz_gst.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["finbyz_gst.utils.before_request"]
# after_request = ["finbyz_gst.utils.after_request"]

# Job Events
# ----------
# before_job = ["finbyz_gst.utils.before_job"]
# after_job = ["finbyz_gst.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
#	{
#		"doctype": "{doctype_1}",
#		"filter_by": "{filter_by}",
#		"redact_fields": ["{field_1}", "{field_2}"],
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_2}",
#		"filter_by": "{filter_by}",
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_3}",
#		"strict": False,
#	},
#	{
#		"doctype": "{doctype_4}"
#	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#	"finbyz_gst.auth.validate"
# ]

from india_compliance.gst_india.api_classes.e_invoice import EInvoiceAPI
from finbyz_gst.api import einvoice_setup
EInvoiceAPI.setup = einvoice_setup

from india_compliance.gst_india.api_classes.e_waybill import EWaybillAPI
from finbyz_gst.api import ewaybill_setup
EWaybillAPI.setup = ewaybill_setup

from india_compliance.gst_india.api_classes.base import BaseAPI
from finbyz_gst.api import get_url
BaseAPI.get_url = get_url

from india_compliance.gst_india.api_classes.public import PublicAPI
from finbyz_gst.api import get_gstin_info
PublicAPI.get_gstin_info = get_gstin_info 

from india_compliance.gst_india.utils.transaction_data import GSTTransactionData
from finbyz_gst.api import update_transaction_tax_details as new_update_transaction_tax_details
GSTTransactionData.update_transaction_tax_details = new_update_transaction_tax_details