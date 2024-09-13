from . import __version__ as app_version

app_name = "mvl"
app_title = "mvl"
app_publisher = "veeramayandi.p@groupteampro.com"
app_description = "CLMS "
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "veeramayandi.p@groupteampro.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
app_include_css = "/assets/mvl/css/mvl.css"
# app_include_js = "/assets/mvl/js/mvl.js"

# include js, css files in header of web template
# web_include_css = "/assets/mvl/css/mvl.css"
# web_include_js = "/assets/mvl/js/mvl.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "mvl/public/scss/website"

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

# Installation
# ------------

# before_install = "mvl.install.before_install"
# after_install = "mvl.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "mvl.uninstall.before_uninstall"
# after_uninstall = "mvl.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "mvl.notifications.get_notification_config"

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

doc_events = {
	"Salary Slip":{
		"after_insert":"mvl.custom.get_total_payable_to_mvl",
        "on_submit":"mvl.mvl.doctype.monthly_invoice_processing.monthly_invoice_processing.process_invoice_arrear",
        "on_cancel":"mvl.mvl.doctype.monthly_invoice_processing.monthly_invoice_processing.revert_the_slip",
		"validate":["mvl.custom.get_total_payable_to_mvl","mvl.custom.salary_slip_validate"]
	},
	"Attendance and OT Register":{
		"on_submit":["mvl.custom.update_ncp","mvl.custom.update_casual_leave"],
		"before_save": "mvl.custom.validate_dat",
		"on_cancel" : ["mvl.custom.cancel_update_casual_leave"]
	},
    "Payroll Entry":{
		"before_save": "mvl.custom.validate_arrear_or_not",
	},
	"Employee":{
		"after_insert": "mvl.custom.get_contract_end_date",
		"validate": "mvl.custom.inactive_employee",
	},
	
	# "Arrear Salary Updation":{
	# 	"after_insert":"mvl.custom.get_tott_ncp",
	# },
	# "Salary Detail":{
	# 	"after_insert":"mvl.custom.get_sub_total",
	# },

}

# Scheduled Tasks
# ---------------

scheduler_events = {
#	"all": [
#		"mvl.tasks.all"
#	],
#	"daily": [
#		"mvl.tasks.daily"
#	],
#	"hourly": [
#		"mvl.tasks.hourly"
#	],
#	"weekly": [
#		"mvl.tasks.weekly"
#	]
	# "daily": [
	# 	"mvl.mvl.doctype.employee_casual_leave.employee_casual_leave.update_total_leaves_allocated"
	# ]
	"cron":{
		"30 00 * * *" :[
			'mvl.custom.update_total_leaves_allocated'
		],
		"01 00 * * *" :[
			'hrms.payroll.doctype.salary_slip.salary_slip.email_salary_slip'
		],
	}
}

# Testing
# -------

# before_tests = "mvl.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "mvl.event.get_events"
# }
jinja = {
	"methods": [
		"mvl.custom.get_data_for_annexture"
	]
}

#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task": "mvl.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

user_data_fields = [
	{
		"doctype": "{doctype_1}",
		"filter_by": "{filter_by}",
		"redact_fields": ["{field_1}", "{field_2}"],
		"partial": 1,
	},
	{
		"doctype": "{doctype_2}",
		"filter_by": "{filter_by}",
		"partial": 1,
	},
	{
		"doctype": "{doctype_3}",
		"strict": False,
	},
	{
		"doctype": "{doctype_4}"
	}
]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#	"mvl.auth.validate"
# ]

