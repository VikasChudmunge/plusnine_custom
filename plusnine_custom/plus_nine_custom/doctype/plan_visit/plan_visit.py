# Copyright (c) 2025, sanprasoftwares@gmail.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils.nestedset import get_descendants_of



class PlanVisit(Document):

	@frappe.whitelist()
	def single_record(self):
		if self.doctype_name == "Lead":
			lead_doc = frappe.get_doc("Lead", self.id)
			self.append("items", {
				"doctype_name": "Lead",
				"id": lead_doc.name,
				"name1": lead_doc.first_name,
				"email": lead_doc.email_id,
				"phone": lead_doc.mobile_no
			})
		if self.doctype_name == "Prospect":
			prospect_doc = frappe.get_doc("Prospect", self.id)
			self.append("items", {
				"doctype_name": "Prospect",
				"id": prospect_doc.name,
				"name1": prospect_doc.company_name,
				"email": prospect_doc.custom_email,
				"phone": prospect_doc.custom_phone
			})
		if self.doctype_name == "Customer":
			customer_doc = frappe.get_doc("Customer", self.id)
			self.append("items", {
				"doctype_name": "Customer",
				"id": customer_doc.name,
				"name1": customer_doc.customer_name,
				"email": customer_doc.email_id,
				"phone": customer_doc.mobile_no
			})
		if self.doctype_name == "Quotation":
			quotation_doc = frappe.get_doc("Quotation", self.id)
			self.append("items", {
				"doctype_name": "Quotation",
				"id": quotation_doc.name,
				"name1": quotation_doc.title,
				"email": quotation_doc.contact_email,
				"phone": quotation_doc.contact_mobile
			})
		if self.doctype_name == "Opportunity":
			opportunity_doc = frappe.get_doc("Opportunity", self.id)
			self.append("items", {
				"doctype_name": "Opportunity",
				"id": opportunity_doc.name,
				"name1": opportunity_doc.title,
				"email": opportunity_doc.contact_email,
				"phone": opportunity_doc.phone
			})
	
	@frappe.whitelist() 
	def add_items_child(self):
		doc_filter = {}

		if self.form_date and self.to_date:
			doc_filter["creation"] = ["between", [self.form_date, self.to_date]]
		if self.brand:
			doc_filter["custom_brand"] = self.brand 
		# if self.territory:
		# 	doc_filter["territory"] = self.territory

		if self.territory:
			child_territories = get_descendants_of("Territory", self.territory)
			child_territories.append(self.territory)
			doc_filter["territory"] = ["in", child_territories]
		
		if self.customer_group:
			doc_filter["custom_customer_group"] = self.customer_group
		if self.prospect_customer_group:
			doc_filter["customer_group"] = self.prospect_customer_group
			


		doc_name = {
			"Lead": "name",
			"Prospect": "name",
			"Customer": "name",
			"Quotation": "name",
			"Opportunity": "name"
		}
		field_name = {
			"Lead": "first_name",
			"Prospect": "company_name",
			"Customer": "customer_name",
			"Quotation": "title",
			"Opportunity": "title"
		}
		field_firstname = {
			"Lead": "first_name",
			"Prospect": "company_name",
			"Customer": "customer_name",
			"Quotation": "party_name",
			"Opportunity": "party_name"
		}

		field_email = {
			"Lead": "email_id",
			"Prospect": "custom_email",
			"Customer": "email_id",
			"Quotation": "contact_email",
			"Opportunity": "contact_email"
		}

		field_phone = {
			"Lead": "mobile_no",
			"Prospect": "custom_phone",
			"Customer": "mobile_no",
			"Quotation": "contact_mobile",
			"Opportunity": "phone"
		}

		docname = doc_name.get(self.doctype_name) 
		fieldname = field_name.get(self.doctype_name) 
		firstname = field_firstname.get(self.doctype_name) 
		fieldemail = field_email.get(self.doctype_name) 
		fieldphone = field_phone.get(self.doctype_name) 
		# frappe.throw(str(doc_filter))

		data = frappe.get_all(self.doctype_name, filters=doc_filter, fields=[docname,firstname, fieldemail, fieldphone])
		for row in data:
			self.append("items", {
				"doctype_name": self.doctype_name,
				"id": row.get(docname),
				"name1": row.get(firstname),
				"email": row.get(fieldemail),  
				"phone": row.get(fieldphone)
			})
		# frappe.throw(str(data))
	


	def on_submit(self):
		# self.create_field_visit() 
		self.create_field_visits_docs()
	
	# @frappe.whitelist()
	# def create_field_visit(self):
	# 	new_doc = frappe.new_doc("Field Visit") 
	# 	new_doc.plan_visit_id = self.name

	# 	for row in self.get("items"):  ##,{"add_rows":1}
	# 		new_doc.append("items", {  
	# 			"doctype_name": row.doctype_name,
	# 			"id": row.id,
	# 			"name1": row.name1,  
	# 			"phone": row.phone,
	# 			"email": row.email
	# 		})
		
	# 	if new_doc.items:
	# 		new_doc.save()
	# 		self.load_from_db() 
			# self.reload()
	

	# Create Field Visits Doc
	@frappe.whitelist()
	def create_field_visits_docs(self):

		for row in self.get("items"):  ##,{"add_rows":1}
			new_doc = frappe.new_doc("Field Visits")
			new_doc.plan_visit_id = self.name
			new_doc.allocated_to = self.allocated_to
			new_doc.doctype_name= row.doctype_name
			new_doc.name1= row.name1
			new_doc.id= row.id	
			new_doc.phone= row.phone
			new_doc.email= row.email

			new_doc.save()
			self.load_from_db()


from frappe.utils import now_datetime, get_datetime
import frappe

@frappe.whitelist()
def recurring_plan():
	plan_visits = frappe.get_all(
		"Plan Visit", 
		filters={"is_recurring": 1, "docstatus": 1}, 
		fields=["field_visit_frequency", "name"]
	)

	# frequencies in seconds 
	frequencies = {
		"Daily": 60 * 60 * 24,         # 86400 seconds
		"Weekly": 60 * 60 * 24 * 7,    # 604800 seconds
		"Monthly": 60 * 60 * 24 * 30,  # 2592000 seconds (~30 days)
		"Yearly": 60 * 60 * 24 * 365   # 31536000 seconds (~365 days)
	}

	nowtime = now_datetime()

	# frappe.throw(str(plan_visits))
	for plan_visit in plan_visits:
		field_visit = frappe.get_all(
			"Field Visits", 
			filters={"plan_visit_id": plan_visit.name},
			order_by="creation desc",
			# limit_page_length=1,
			fields=["creation"]
		)
		# frappe.throw(str(field_visit))
	
 
		if field_visit:
			last_visit_time = get_datetime(field_visit[0].creation)
			seconds_diff = (nowtime - last_visit_time).total_seconds()

			# frappe.throw(str(seconds_diff))
			if seconds_diff >= frequencies.get(plan_visit.field_visit_frequency, 0):
				create_field_visit(plan_visit.name)


@frappe.whitelist()
def create_field_visit(pv_id):
	pv_doc = frappe.get_doc("Plan Visit",pv_id)
	for row in pv_doc.items:
		new_doc = frappe.new_doc("Field Visits")
		new_doc.plan_visit_id = pv_id
		new_doc.allocated_to = pv_doc.allocated_to
		new_doc.doctype_name= row.doctype_name
		new_doc.name1= row.name1
		new_doc.id= row.id	
		new_doc.phone= row.phone
		new_doc.email= row.email
		new_doc.save()

# @frappe.whitelist()
# def create_field_visit(pv_id):
# 	pv_doc = frappe.get_doc("Plan Visit",pv_id)
# 	new_doc = frappe.new_doc("Field Visit")
# 	new_doc.plan_visit_id = pv_id

# 	for row in pv_doc.items:
# 		new_doc.append("items", {
# 			"doctype_name": row.doctype_name,
# 			"id": row.id,
# 			"name1": row.name1,
# 			"phone": row.phone,
# 			"email": row.email
# 		})

# 	new_doc.save()





	



  

	