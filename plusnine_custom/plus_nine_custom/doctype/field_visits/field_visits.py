# Copyright (c) 2025, sanprasoftwares@gmail.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class FieldVisits(Document):

	def on_submit(self):
		self.get_session_user()

	@frappe.whitelist()
	def get_session_user(self):
		# frappe.throw(str(frappe.session.user))
		self.visited_by = frappe.session.user
		# frappe.set_value("Field Visits", self.name, "allocated_to", frappe.session.user) 