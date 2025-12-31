// Copyright (c) 2025, sanprasoftwares@gmail.com and contributors
// For license information, please see license.txt

frappe.query_reports["Item Price Check"] = {
	 "filters": [
        {
            "fieldname": "item",
            "label": __("Item"),
            "fieldtype": "Link",
            "options": "Item",
            "reqd": 0,
			on_change: function () {
                let item = frappe.query_report.get_filter_value("item");
                if (item) {
                    frappe.query_report.set_filter_value("item_group", "");
                }
            }
        },
        {
            "fieldname": "item_group",
            "label": __("Item Group"),
            "fieldtype": "Link",
            "options": "Item Group",
            "reqd": 0,
			on_change: function () {
                let item_group = frappe.query_report.get_filter_value("item_group");
                if (item_group) {
                    frappe.query_report.set_filter_value("item", "");
                }
            }
        }
    ]
};
  