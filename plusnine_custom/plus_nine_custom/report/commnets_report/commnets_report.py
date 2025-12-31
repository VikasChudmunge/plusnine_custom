import frappe

def execute(filters=None):
	if not filters:
		filters = {}

	columns = get_columns()
	data = []

	# 🔹 Base filters
	comment_filters = {
		"comment_type": "Comment",
		"reference_doctype": ["in", ["Lead", "Opportunity", "Customer", "Prospect"]],
	}

	# 🔹 Apply date range
	from_date = filters.get("from_date")
	to_date = filters.get("to_date")

	if from_date and to_date:
		comment_filters["creation"] = ["between", [from_date, to_date]]
	elif from_date:
		comment_filters["creation"] = [">=", from_date]
	elif to_date:
		comment_filters["creation"] = ["<=", to_date]

	# 🔹 Apply document type filter (Lead / Opportunity / Customer / Prospect)
	if filters.get("document_type"):
		comment_filters["reference_doctype"] = filters.get("document_type")

	if filters.get("comment_by"):
		comment_filters["comment_by"] = filters.get("comment_by")

	# 🔹 Fetch comments 
	comments = frappe.get_all(
		"Comment",
		filters=comment_filters,
		fields=["name as comment_name", "reference_doctype", "reference_name", "content", "creation"],
		order_by="creation desc",
	)

	for c in comments:
		mobile_no = ""
		brand = ""
		customer_name = ""

		# 🔹 For Lead
		if c.reference_doctype == "Lead":
			lead = frappe.db.get_value(
				"Lead",
				c.reference_name,
				["mobile_no", "custom_brand", "lead_name"],
				as_dict=True,
			)
			if lead:
				mobile_no = lead.mobile_no or ""
				brand = lead.custom_brand or ""
				customer_name = lead.lead_name or ""

		# 🔹 For Opportunity
		elif c.reference_doctype == "Opportunity":
			opp = frappe.db.get_value(
				"Opportunity",
				c.reference_name,
				["phone", "custom_brand", "customer_name"],
				as_dict=True,
			)
			if opp:
				mobile_no = opp.phone or ""
				brand = opp.custom_brand or ""
				customer_name = opp.customer_name or ""

		# 🔹 For Customer
		elif c.reference_doctype == "Customer":
			cust = frappe.db.get_value(
				"Customer",
				c.reference_name,
				["mobile_no", "customer_name"],
				as_dict=True,
			)
			if cust:
				mobile_no = cust.mobile_no or ""
				customer_name = cust.customer_name or ""

		# 🔹 For Prospect
		elif c.reference_doctype == "Prospect":
			prosp = frappe.db.get_value(
				"Prospect",
				c.reference_name,
				["custom_phone", "company_name"],
				as_dict=True,
			)
			if prosp:
				mobile_no = prosp.custom_phone or ""
				customer_name = prosp.company_name or ""

		data.append([
			c.comment_name,
			c.reference_doctype,
			c.reference_name,
			c.content,
			mobile_no,
			brand,
			customer_name,
			c.creation,
		])

	return columns, data


def get_columns():
	return [
		{"label": "Comment ID", "fieldname": "comment_name", "fieldtype": "Link", "options": "Comment", "width": 160},
		{"label": "Reference Doctype", "fieldname": "reference_doctype", "fieldtype": "Data", "width": 130},
		{"label": "Reference Name", "fieldname": "reference_name", "fieldtype": "Dynamic Link", "options": "reference_doctype", "width": 150},
		{"label": "Content", "fieldname": "content", "fieldtype": "Text", "width": 250},
		{"label": "Mobile No", "fieldname": "mobile_no", "fieldtype": "Data", "width": 120},
		{"label": "Brand", "fieldname": "brand", "fieldtype": "Data", "width": 120},
		{"label": "Customer Name", "fieldname": "customer_name", "fieldtype": "Data", "width": 150},
		{"label": "Created On", "fieldname": "creation", "fieldtype": "Datetime", "width": 160},
	]


def get_report_filters():
	return [
		{
			"fieldname": "from_date",
			"label": "From Date",
			"fieldtype": "Date",
			"default": frappe.utils.add_days(frappe.utils.nowdate(), -30),
		},
		{
			"fieldname": "to_date",
			"label": "To Date",
			"fieldtype": "Date",
			"default": frappe.utils.nowdate(),
		},
		{
			"fieldname": "document_type",
			"label": "Document Type",
			"fieldtype": "Select",
			"options": "\nLead\nOpportunity\nCustomer\nProspect",
			"default": "Lead",
		},
	]
