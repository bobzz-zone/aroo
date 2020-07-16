# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "Aroo"
app_title = "Aroo"
app_publisher = "bobzz.zone@gmail.com"
app_description = "For Styling"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "bobzz.zone@gmail.com"
app_license = "MIT"
app_logo_url ="/assets/aroo/images/logo_icon.png"
#website_context = {
#	"favicon": 	"assets/aroo/images/small.png",
#	"splash_image": "assets/aroo/images/big.png"
#}
# Includes in <head>
# ------------------
#app_include_css = "assets/css/aroo.min.css"
#app_include_js = "assets/js/aroo.min.js"
#web_include_css = "assets/css/aroo.min.css"
# include js, css files in header of desk.html
# app_include_css = "/assets/aroo/css/aroo.css"
# app_include_js = "/assets/aroo/js/aroo.js"

# include js, css files in header of web template
# web_include_css = "/assets/aroo/css/aroo.css"
# web_include_js = "/assets/aroo/js/aroo.js"
setup_wizard_requires = "assets/aroo/js/setup_wizard.js"
#setup_wizard_stages = "aroo.setup_wizard.get_setup_stages"
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

# Website user home page (by function)
# get_website_user_home_page = "aroo.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "aroo.install.before_install"
after_install = "aroo.custom_function.after_install"
on_login="aroo.custom_function.login_block"
# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "aroo.notifications.get_notification_config"

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

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"User": {
		"validate": "aroo.custom_function.validate_user_quota",
		"before_insert": "aroo.custom_function.set_block_module"
		# "on_submit" : my_account.doctype.sync_server_settings.create_new_user
	}
}

# on_session_creation =[
# 	"aroo.custom_function.login_block"
# ]
# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"aroo.tasks.all"
# 	],
# 	"daily": [
# 		"aroo.tasks.daily"
# 	],
# 	"hourly": [
# 		"aroo.tasks.hourly"
# 	],
# 	"weekly": [
# 		"aroo.tasks.weekly"
# 	]
# 	"monthly": [
# 		"aroo.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "aroo.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "aroo.event.get_events"
# }

