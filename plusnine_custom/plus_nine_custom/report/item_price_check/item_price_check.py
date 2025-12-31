import frappe

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data


def get_columns():
    return [
        {"label": "Item Code", "fieldname": "item_code", "fieldtype": "Link", "options": "Item", "width": 150},
        {"label": "Item Name", "fieldname": "item_name", "fieldtype": "Data", "width": 180},
        {"label": "Brand", "fieldname": "brand", "fieldtype": "Data", "width": 120},
        {"label": "Price List", "fieldname": "price_list", "fieldtype": "Link", "options": "Price List", "width": 150},
        {"label": "Rate", "fieldname": "rate", "fieldtype": "Currency", "width": 120},
    ]


def get_data(filters):
    data = []

    # Case 1: Filter by Item
    if filters.get("item"):
        item_price_list = frappe.get_all(
            "Item Price",
            {"item_code": filters.get("item")},
            ["item_code", "item_name", "brand", "price_list", "price_list_rate"]
        )

        parent_shown = False
        for row in item_price_list:
            data.append({
                "item_code": row.item_code if not parent_shown else "",
                "item_name": row.item_name if not parent_shown else "",
                "brand": row.brand if not parent_shown else "",
                "price_list": row.price_list,
                "rate": row.price_list_rate
            })
            parent_shown = True

    # Case 2: Filter by Item Group
    elif filters.get("item_group"):
        items = frappe.get_all("Item", {"item_group": filters.get("item_group")}, ["item_code", "item_name", "brand"])

        for item in items:
            price_list = frappe.get_all(
                "Item Price",
                {"item_code": item.item_code},
                ["item_code", "item_name", "brand", "price_list", "price_list_rate"]
            )

            parent_shown = False
            for row in price_list:
                data.append({
                    "item_code": row.item_code if not parent_shown else "",
                    "item_name": row.item_name if not parent_shown else "",
                    "brand": row.brand if not parent_shown else "",
                    "price_list": row.price_list,
                    "rate": row.price_list_rate
                })
                parent_shown = True

    return data
