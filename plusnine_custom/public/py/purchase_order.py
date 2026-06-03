import frappe

@frappe.whitelist()
def create_multiple_batch(doc, method=None):
    # frappe.throw("Hii")
    items = []
    for item in doc.items:
        has_multiple_batch = frappe.get_value("Item", item.item_code, "custom_has_multiple_batch")
        # Only apply splitting logic for item "Mobile"
        if has_multiple_batch == 1 and item.qty > 1 and frappe.db.get_value("Item", item.item_code, "create_new_batch"):
            original_qty = int(item.qty)
            
            # First row: keep 1 qty
            item.qty = 1 
            item.received_qty = 1
            item.batch_no = None
            item.serial_and_batch_bundle = None
            items.append(item)
            
            # Add remaining rows with qty 1 each
            for i in range(1, original_qty):
                new_row = frappe.copy_doc(item)
                new_row.name = None
                new_row.qty = 1
                new_row.received_qty = 1
                new_row.batch_no = None
                new_row.serial_and_batch_bundle = None
                items.append(new_row)
        else:
            # Normal behavior for all other items
            items.append(item)

    doc.items = items