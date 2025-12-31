// Copyright (c) 2025, sanprasoftwares@gmail.com and contributors
// For license information, please see license.txt

frappe.query_reports["Custom Sales Order Trends"] = {
	"filters": [
		{
			fieldname: "period",
			label: __("Period"),
			fieldtype: "Select",
			options: [
				{ value: "Monthly", label: __("Monthly") },
				{ value: "Quarterly", label: __("Quarterly") },
				{ value: "Half-Yearly", label: __("Half-Yearly") },
				{ value: "Yearly", label: __("Yearly") },
			],
			default: "Monthly",
		},
		{
			fieldname: "based_on",
			label: __("Based On"),
			fieldtype: "Select",
			options: [
				{ value: "Item", label: __("Item") },
				{ value: "Item Group", label: __("Item Group") },
				{ value: "Customer", label: __("Customer") },
				{ value: "Customer Group", label: __("Customer Group") },
				{ value: "Territory", label: __("Territory") },
				{ value: "Project", label: __("Project") },
			],
			default: "Item",
			dashboard_config: {
				read_only: 1,
			},
		},
		{
			fieldname: "group_by",
			label: __("Group By"),
			fieldtype: "Select",
			options: ["", { value: "Item", label: __("Item") }, { value: "Customer", label: __("Customer") }],
			default: "",
		},
		{
			fieldname: "fiscal_year",
			label: __("Fiscal Year"),
			fieldtype: "Link",
			options: "Fiscal Year",
			default: erpnext.utils.get_fiscal_year(frappe.datetime.get_today()),
		},
		{
			fieldname: "company",
			label: __("Company"),
			fieldtype: "Link",
			options: "Company",
			default: frappe.defaults.get_user_default("Company"),
		},
		{
			fieldname: "cost_center",
			label: __("Cost Center"),
			fieldtype: "Link",
			options: "Cost Center"
		}
	]
};

// frappe.query_reports["Custom Sales Order Trends"] = $.extend({}, erpnext.sales_trends_filters);

// frappe.query_reports["Custom Sales Order Trends"]["filters"].push(
// 	{
// 	fieldname: "include_closed_orders",
// 	label: __("Include Closed Orders"),
// 	fieldtype: "Check",
// 	default: 0,
// 	},
// 	{
// 		fieldname: "cost_center",
// 		label: __("Cost Center"),
// 		fieldtype: "Link",
// 		options: "Cost Center"
// 	}
// );  



