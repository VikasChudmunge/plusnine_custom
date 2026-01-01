// Copyright (c) 2025, sanprasoftwares@gmail.com and contributors
// For license information, please see license.txt

frappe.query_reports["Brand Wise Custom Sales Report"] = {
	"filters": [
        {
            fieldname: "group_by",
            label: "Group By",
            fieldtype: "Select",
            options: "Brand\nCost Center",
            default: "Brand"
        },
        {
            fieldname: "brand",
            label: "Brand",
            fieldtype: "Link",
            options: "Brand",
            depends_on: "eval:doc.group_by == 'Brand'" 
        },
        {  
            fieldname: "cost_center",
            label: "Cost Center",
            fieldtype: "Link",
            options: "Cost Center",
            depends_on: "eval:doc.group_by == 'Cost Center'"
        }
    ]
};
 