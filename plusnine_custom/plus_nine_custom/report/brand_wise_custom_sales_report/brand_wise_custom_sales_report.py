
# import frappe
# from frappe.utils import today, getdate, get_first_day

# def execute(filters=None):
#     columns = get_columns()
#     data = get_data() 
#     return columns, data


# def get_columns():
#     return [
#         {"label": "Brand", "fieldname": "brand", "fieldtype": "Data", "width": 200},
#         # {"label": "Total Sales", "fieldname": "total_sales", "fieldtype": "Currency", "width": 150},
#         {"label": "Today's Sales", "fieldname": "today_sales", "fieldtype": "Currency", "width": 150},
#         {"label": "Current Month Sales", "fieldname": "month_sales", "fieldtype": "Currency", "width": 180},
#         {"label": "Year To Date Sales", "fieldname": "ytd_sales", "fieldtype": "Currency", "width": 180}
#     ]
 

# def get_data():
#     today_date = getdate(today())
#     month_start = get_first_day(today_date)        # 1st day of current month
#     year_start = getdate(f"{today_date.year}-01-01")

#     query = """
#         SELECT
#             i.brand AS brand,

#             SUM(soi.base_net_amount) AS total_sales,

#             SUM(
#                 CASE
#                     WHEN so.transaction_date = %(today)s
#                     THEN soi.base_net_amount
#                     ELSE 0
#                 END
#             ) AS today_sales,

#             SUM(
#                 CASE
#                     WHEN so.transaction_date BETWEEN %(month_start)s AND %(today)s
#                     THEN soi.base_net_amount
#                     ELSE 0
#                 END
#             ) AS month_sales,

#             SUM(
#                 CASE
#                     WHEN so.transaction_date BETWEEN %(year_start)s AND %(today)s
#                     THEN soi.base_net_amount
#                     ELSE 0
#                 END
#             ) AS ytd_sales

#         FROM `tabSales Order` so
#         INNER JOIN `tabSales Order Item` soi ON soi.parent = so.name
#         INNER JOIN `tabItem` i ON i.name = soi.item_code

#         WHERE
#             so.docstatus = 1
#             AND i.brand IS NOT NULL

#         GROUP BY i.brand
#         ORDER BY total_sales DESC
#     """

#     return frappe.db.sql(
#         query,
#         {
#             "today": today_date,
#             "month_start": month_start,
#             "year_start": year_start
#         },
#         as_dict=True
#     )



import frappe
from frappe.utils import today, getdate, get_first_day

def execute(filters=None):
    filters = filters or {}
    columns = get_columns(filters)
    data = get_data(filters)
    return columns, data


def get_columns(filters):
    group_by = filters.get("group_by", "Brand")

    first_col_label = "Brand" if group_by == "Brand" else "Cost Center"

    base_columns = [
        {
            "label": first_col_label,
            "fieldname": "group_value",
            "fieldtype": "Data",
            "width": 200
        },
        {"label": "Today's Sales", "fieldname": "today_sales", "fieldtype": "Currency", "width": 150},
        {"label": "Current Month Sales", "fieldname": "month_sales", "fieldtype": "Currency", "width": 180},
        {"label": "Year To Date Sales", "fieldname": "ytd_sales", "fieldtype": "Currency", "width": 180}
    ]

    if group_by == "Cost Center":
        base_columns.extend(
            [
                {"label": "Others Today", "fieldname": "others_today", "fieldtype": "Currency", "width": 150},
                {"label": "Others Current Month", "fieldname": "others_month", "fieldtype": "Currency", "width": 180},
                {"label": "Others YTD", "fieldname": "others_ytd", "fieldtype": "Currency", "width": 180},
                {"label": "P91 - Others Today", "fieldname": "p91_minus_others_today", "fieldtype": "Currency", "width": 180},
                {"label": "P91 - Others Current Month", "fieldname": "p91_minus_others_month", "fieldtype": "Currency", "width": 200},
                {"label": "P91 - Others YTD", "fieldname": "p91_minus_others_ytd", "fieldtype": "Currency", "width": 180},
            ]
        )

    return base_columns


def get_data(filters):
    today_date = getdate(today())
    month_start = get_first_day(today_date)
    year_start = getdate(f"{today_date.year}-01-01")

    group_by = filters.get("group_by", "Brand")

    # Dynamic grouping
    if group_by == "Cost Center":
        group_field = "so.cost_center"
        group_condition = "AND so.cost_center = %(cost_center)s" if filters.get("cost_center") else ""
    else:
        group_field = "i.brand"
        group_condition = "AND i.brand = %(brand)s" if filters.get("brand") else ""
        group_condition += " AND i.brand != %(excluded_brand)s"

    query = f"""
        SELECT
            {group_field} AS group_value,

            SUM(
                CASE
                    WHEN so.transaction_date = %(today)s
                    THEN soi.base_net_amount
                    ELSE 0
                END
            ) AS today_sales,

            SUM(
                CASE
                    WHEN so.transaction_date BETWEEN %(month_start)s AND %(today)s
                    THEN soi.base_net_amount
                    ELSE 0
                END
            ) AS month_sales,

            SUM(
                CASE
                    WHEN so.transaction_date BETWEEN %(year_start)s AND %(today)s
                    THEN soi.base_net_amount
                    ELSE 0
                END
            ) AS ytd_sales

        FROM `tabSales Order` so
        INNER JOIN `tabSales Order Item` soi ON soi.parent = so.name
        INNER JOIN `tabItem` i ON i.name = soi.item_code

        WHERE
            so.docstatus = 1
            {group_condition}

        GROUP BY {group_field}
        ORDER BY ytd_sales DESC
    """

    rows = frappe.db.sql(
        query,
        {
            "today": today_date,
            "month_start": month_start,
            "year_start": year_start,
            "brand": filters.get("brand"),
            "cost_center": filters.get("cost_center"),
            "excluded_brand": "P91 CC"
        },
        as_dict=True
    )

    if group_by != "Cost Center":
        return rows

    p91_label = "P91 Car care - P91"
    p91_row = next((row for row in rows if row.get("group_value") == p91_label), None)
    others_rows = [row for row in rows if row.get("group_value") != p91_label]

    others_today = sum(row.get("today_sales") or 0 for row in others_rows)
    others_month = sum(row.get("month_sales") or 0 for row in others_rows)
    others_ytd = sum(row.get("ytd_sales") or 0 for row in others_rows)

    p91_today = (p91_row or {}).get("today_sales") or 0
    p91_month = (p91_row or {}).get("month_sales") or 0
    p91_ytd = (p91_row or {}).get("ytd_sales") or 0

    return [
        {
            "group_value": p91_label,
            "today_sales": p91_today,
            "month_sales": p91_month,
            "ytd_sales": p91_ytd,
            "others_today": others_today,
            "others_month": others_month,
            "others_ytd": others_ytd,
            "p91_minus_others_today": p91_today - others_today,
            "p91_minus_others_month": p91_month - others_month,
            "p91_minus_others_ytd": p91_ytd - others_ytd,
        }
    ]
