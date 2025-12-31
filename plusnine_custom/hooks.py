app_name = "plusnine_custom"
app_title = "Plus Nine Custom"
app_publisher = "sanprasoftwares@gmail.com"
app_description = "Plus Nine Custom"
app_email = "sanprasoftwares@gmail.com"
app_license = "mit"

# Apps
# ------------------
# stunted apps will not be installed until all their dependencies are installed
# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "plusnine_custom",
# 		"logo": "/assets/plusnine_custom/logo.png",
# 		"title": "Plus Nine Custom",
# 		"route": "/plusnine_custom",
# 		"has_permission": "plusnine_custom.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/plusnine_custom/css/plusnine_custom.css"
# app_include_js = "/assets/plusnine_custom/js/plusnine_custom.js"

# include js, css files in header of web template
# web_include_css = "/assets/plusnine_custom/css/plusnine_custom.css"
# web_include_js = "/assets/plusnine_custom/js/plusnine_custom.js"
# app_include_css = "/assets/plusnine_custom/css/custom_login.css"
# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "plusnine_custom/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

doctype_js = {"Lead":"public/js/custom_lead.js",
                "Prospect":"public/js/custom_prospect.js",
                "Opportunity":"public/js/custom_opportunity.js",
                "Customer":"public/js/custom_customer.js",
                "Delivery Note":"public/js/custom_delivery.js",
                "Sales Order":"public/js/custom_salesorder.js",
                "Sales Invoice":"public/js/custom_salesinvoice.js",
                "Quotation":"public/js/custom_quotation.js",
                "Job Card":"public/js/custom_jobcard.js",
                # "Sales Order":"public/js/sales_order.js",
                # "Prospect": "public/js/prospect.js",
            }
after_migrate = ["plusnine_custom.custom_pyfile.custom_python.patch_make_packing_list"]

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "plusnine_custom/public/icons.svg"

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
# 	"methods": "plusnine_custom.utils.jinja_methods",
# 	"filters": "plusnine_custom.utils.jinja_filters"
# }
jinja = {
    "methods" : [
      "plusnine_custom.plus_nine_custom.utils.sales_order_print.get_invoice_item_and_tax_details",
      "plusnine_custom.plus_nine_custom.utils.sales_invoice_print.get_inv_item_and_tax_details",
      "frappe.utils.data.money_in_words"
    ]
}

# Installation
# ------------

# before_install = "plusnine_custom.install.before_install"
# after_install = "plusnine_custom.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "plusnine_custom.uninstall.before_uninstall"
# after_uninstall = "plusnine_custom.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "plusnine_custom.utils.before_app_install"
# after_app_install = "plusnine_custom.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "plusnine_custom.utils.before_app_uninstall"
# after_app_uninstall = "plusnine_custom.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "plusnine_custom.notifications.get_notification_config"

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
doc_events = {
    "Prospect": {
        "before_save": "plusnine_custom.custom_pyfile.custom_python.before_save",
        "on_trash": "plusnine_custom.custom_pyfile.custom_python.on_trash"
    },
     "Customer": { 
        "before_save": "plusnine_custom.custom_pyfile.custom_python.cust_set_status",
        "on_trash": "plusnine_custom.custom_pyfile.custom_python.cust_del_set_status"
    },
    "Sales Invoice": {
        "on_submit": "plusnine_custom.custom_pyfile.custom_python.salesinvocie_after_save",
        "on_submit": "plusnine_custom.public.py.sales_invoice.send_invoice_email",
        # "on_submit": "plusnine_custom.public.py.sales_invoice.create_and_attach_pdf",
        # "on_update_after_submit": "plusnine_custom.public.py.sales_invoice.create_and_attach_pdf"

    },
    "Delivery Note": {  
        "on_submit": "plusnine_custom.custom_pyfile.custom_python.delivery_note_submit",
    }, 
    "Lead": {
        "after_insert": "plusnine_custom.public.py.custom_lead.assign_sales_partner",
        "on_update": "plusnine_custom.public.py.custom_lead.assign_sales_partner"
    },
    "Sales Partner Assigned Lead": {
        "after_insert": "plusnine_custom.public.py.custom_sales_partner_assign_lead.create_opportunity"
    },
    "Opportunity":{
        "before_save": "plusnine_custom.public.py.opportunity.set_quotation_lost" 
        # "after_save": "plusnine_custom.public.py.opportunity.set_quotation_lost" 
    },
    "ToDo": {
        "after_insert": "plusnine_custom.public.py.todo_webhook.update_due_checkbox",
        "on_update": "plusnine_custom.public.py.todo_webhook.update_due_checkbox"
    },
     "Event": {
        "before_insert": "plusnine_custom.public.py.event.set_event_public"
    }
   
    # "Sales Order": {
    #       "on_submit": "plusnine_custom.public.py.sales_order.create_and_attach_pdf"
    #   #   "on_submit": "plusnine_custom.public.py.sales_order.create_job_cards",
    # },
}
# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

scheduler_events = {
# 	"all": [
# 		"plusnine_custom.tasks.all"
# 	],
# 	"daily": [
# 		"plusnine_custom.tasks.daily"
# 	],
	"hourly": [
		"plusnine_custom.plus_nine_custom.doctype.plan_visit.plan_visit.recurring_plan"
	],
    "daily": [
        "plusnine_custom.public.py.notification.send_todo_summary",
        "plusnine_custom.public.py.notification.send_due_date_reminder",
        "plusnine_custom.public.py.notification.send_overdue_todos",
        "plusnine_custom.public.py.todo_webhook.check_due_todos",
    ],
    "cron": { 
        "59 23 * * *": [
            "plusnine_custom.public.py.notification.send_camping_wise_lead_report_html",
            "plusnine_custom.public.py.notification.brand_costcenter_sales_mail"
        ]
    }

# 	"weekly": [
# 		"plusnine_custom.tasks.weekly"
# 	],
# 	"monthly": [
# 		"plusnine_custom.tasks.monthly"
# 	],
}

# Testing
# -------

# before_tests = "plusnine_custom.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "plusnine_custom.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "plusnine_custom.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]
ignore_links_on_delete = ["Job Cards"]

# Request Events
# ----------------
# before_request = ["plusnine_custom.utils.before_request"]
# after_request = ["plusnine_custom.utils.after_request"]

# Job Events
# ----------
# before_job = ["plusnine_custom.utils.before_job"]
# after_job = ["plusnine_custom.utils.after_job"]

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
# 	"plusnine_custom.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

