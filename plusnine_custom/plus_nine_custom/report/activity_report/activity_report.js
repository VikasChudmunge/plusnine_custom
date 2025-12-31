// Copyright (c) 2025, sanprasoftwares@gmail.com and contributors
// For license information, please see license.txt

frappe.query_reports["Activity Report"] = {
	"filters": [
		{
			"fieldname": "user_name",
			"label": "User Name",
			"fieldtype": "Link",
			"options": "User"
		},
		{  
			"fieldname": "from_date",
			"label": "From Date",
			"fieldtype": "Date",
			default: frappe.datetime.get_today(),
            reqd: 1
		},
		{  
			"fieldname": "to_date",
			"label": "To Date",
			"fieldtype": "Date",
			default: frappe.datetime.get_today(),
            reqd: 1
		}
	]
};
  