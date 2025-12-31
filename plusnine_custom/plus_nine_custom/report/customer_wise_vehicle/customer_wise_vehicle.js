// Copyright (c) 2025, sanprasoftwares@gmail.com and contributors
// For license information, please see license.txt

frappe.query_reports["Customer Wise Vehicle"] = {
	"filters": [
		{
			"fieldname": "from_date",
			"label": "From Date",
			"fieldtype": "Date"
		},
		{
			"fieldname": "to_date", 
			"label": "To Date",
			"fieldtype": "Date"
		},
		{
			"fieldname": "vehicle_type",
			"label": "Vehicle Type",
			"fieldtype": "Link",
			"options": "Customer Wise Vehicle",
			"reqd": 0
		},
		{
			"fieldname": "brand",
			"label": "Brand",
			"fieldtype": "Data",
			"reqd": 0
		},
		{
			"fieldname": "model",
			"label": "Model",
			"fieldtype": "Data",
			"reqd": 0
		},
		{
			"fieldname": "category",
			"label": "Category",
			"fieldtype": "Data",
			"reqd": 0
		}
	]
};
  