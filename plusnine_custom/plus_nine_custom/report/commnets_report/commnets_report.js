// Copyright (c) 2025, sanprasoftwares@gmail.com and contributors
// For license information, please see license.txt

frappe.query_reports["Commnets Report"] = {
	"filters": [
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.add_days(frappe.datetime.get_today(), -1),
		},
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today(),
		},
		{
			"fieldname": "document_type",
			"label": __("Document Type"),
			"fieldtype": "Select",
			"options": "\nLead\nOpportunity\nProspect\nCustomer",
		},
		{
			"fieldname": "comment_by",
			"label": __("Commented By"),
			"fieldtype": "Select",
			"options": "\nAdministrator", 
		},
		 
	]
};
 