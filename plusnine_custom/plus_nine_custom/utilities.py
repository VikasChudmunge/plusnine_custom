import frappe
@frappe.whitelist(allow_guest=True)
def get_category_items(category):
    return frappe.get_all('Category Item', filters={'parent': category}, pluck='item')