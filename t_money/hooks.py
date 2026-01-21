app_name = "t_money"
app_title = "T-Money"
app_publisher = "Alon Ben Refael"
app_description = "Accounting for people with small business (VAT free businesses in Israel)"
app_email = "alonbr@proton.me"
app_license = "mit"
app_logo_url = "/assets/t_money/images/T-money-logo.svg"

website_context = {
	"favicon": "/assets/t_money/images/T-money-logo.svg",
	"splash_image": "/assets/t_money/images/T-money-logo.svg",
#	"footer_powered": 'Powered By <a href="https://frappeframework.com/homepage">Frappe Framework</a>',
#	"copyright": "Created by Alon Ben Refael",
}
# required_apps = []

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
app_include_css = "/assets/t_money/css/t_money.css"
app_include_js = "/assets/t_moneyjs/t_money.js"
# required_apps = []
#app_include_html = [
#	"/templates/includes/global_footer.html"
#]

# Includes in <head>
# ------------------
# include js, css files in header of desk.html
# app_include_css = "/assets/t_money/css/t_money.css"
# app_include_js = "/assets/t_money/js/t_money.js"

# include js, css files in header of web template
# web_include_css = "/assets/t_money/css/t_money.css"
# web_include_js = "/assets/t_money/js/t_money.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "t_money/public/scss/website"

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

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "t_money/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "t_money.utils.jinja_methods",
# 	"filters": "t_money.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "t_money.install.before_install"
after_install = "t_money.install.after_install"
after_migrate = "t_money.install.after_migrate"

# Uninstallation
# ------------

# before_uninstall = "t_money.uninstall.before_uninstall"
# after_uninstall = "t_money.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "t_money.utils.before_app_install"
# after_app_install = "t_money.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "t_money.utils.before_app_uninstall"
# after_app_uninstall = "t_money.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "t_money.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"t_money.tasks.all"
# 	],
# 	"daily": [
# 		"t_money.tasks.daily"
# 	],
# 	"hourly": [
# 		"t_money.tasks.hourly"
# 	],
# 	"weekly": [
# 		"t_money.tasks.weekly"
# 	],
# 	"monthly": [
# 		"t_money.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "t_money.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "t_money.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "t_money.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["t_money.utils.before_request"]
# after_request = ["t_money.utils.after_request"]

# Job Events
# ----------
# before_job = ["t_money.utils.before_job"]
# after_job = ["t_money.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"t_money.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

