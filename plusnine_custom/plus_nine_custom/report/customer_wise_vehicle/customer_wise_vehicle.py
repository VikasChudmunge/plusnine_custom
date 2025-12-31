import frappe

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {"label": "Vehicle Type", "fieldname": "vehicle_type", "fieldtype": "Data", "width": 120},
        {"label": "Count", "fieldname": "vehicle_type_count", "fieldtype": "Int", "width": 100},
        {"label": "Brand", "fieldname": "brand", "fieldtype": "Data", "width": 120},
        {"label": "Count", "fieldname": "brand_count", "fieldtype": "Int", "width": 100},
        {"label": "Model", "fieldname": "model", "fieldtype": "Data", "width": 120},
        {"label": "Count", "fieldname": "model_count", "fieldtype": "Int", "width": 100},
        {"label": "Category", "fieldname": "category", "fieldtype": "Data", "width": 120},
        {"label": "Count", "fieldname": "category_count", "fieldtype": "Int", "width": 100},
    ]

def get_data(filters):
    conditions = ""

    # Apply filters if any
    if filters.get("from_date") and filters.get("to_date"):
        conditions += f" AND creation BETWEEN '{filters['from_date']}' AND '{filters['to_date']}'"
    if filters.get("vehicle_type"):
        conditions += f" AND vehicle_type = '{filters['vehicle_type']}'"
    if filters.get("brand"):
        conditions += f" AND brand = '{filters['brand']}'"
    if filters.get("model"):
        conditions += f" AND model = '{filters['model']}'"
    if filters.get("category"):
        conditions += f" AND category = '{filters['category']}'"

    def get_field_data(field):
        return frappe.db.sql(f"""
            SELECT `{field}` as value, COUNT(*) as count
            FROM `tabCustomer Wise Vehicle`
            WHERE `{field}` IS NOT NULL {conditions}
            GROUP BY `{field}`
            ORDER BY count DESC
        """, as_dict=True)

    vehicle_type_data = get_field_data("vehicle_type")
    brand_data = get_field_data("brand")
    model_data = get_field_data("model")
    category_data = get_field_data("category")

    # Get max rows for padding
    max_len = max(len(vehicle_type_data), len(brand_data), len(model_data), len(category_data))

    data = []
    for i in range(max_len):
        row = {
            "vehicle_type": vehicle_type_data[i]["value"] if i < len(vehicle_type_data) else "",
            "vehicle_type_count": vehicle_type_data[i]["count"] if i < len(vehicle_type_data) else "",

            "brand": brand_data[i]["value"] if i < len(brand_data) else "",
            "brand_count": brand_data[i]["count"] if i < len(brand_data) else "",

            "model": model_data[i]["value"] if i < len(model_data) else "",
            "model_count": model_data[i]["count"] if i < len(model_data) else "",

            "category": category_data[i]["value"] if i < len(category_data) else "",
            "category_count": category_data[i]["count"] if i < len(category_data) else "",
        }
        data.append(row)

    return data
