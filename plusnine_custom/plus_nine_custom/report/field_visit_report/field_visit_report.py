import frappe

def execute(filters=None):
    columns = get_columns()
    data = get_data()
    return columns, data


def get_columns():
    return [
        {
            "label": "Allocated To",
            "fieldname": "allocated_to",
            "fieldtype": "Link",
            "options": "User",
            "width": 200
        },
        {
            "label": "Pending",
            "fieldname": "pending_count",
            "fieldtype": "Int",
            "width": 120
        },
        {
            "label": "Completed",
            "fieldname": "completed_count",
            "fieldtype": "Int",
            "width": 120
        },
        {
            "label": "Today Pending",
            "fieldname": "today_pending",
            "fieldtype": "Int",
            "width": 150
        },
        {
            "label": "Month Pending",
            "fieldname": "month_pending",
            "fieldtype": "Int",
            "width": 150
        }
    ]


def get_data():
    query = """
        SELECT
            allocated_to,

            SUM(CASE WHEN status = 'Pending' THEN 1 ELSE 0 END) AS pending_count,

            SUM(CASE WHEN status = 'Completed' THEN 1 ELSE 0 END) AS completed_count,

            SUM(
                CASE
                    WHEN status = 'Pending'
                    AND DATE(creation) = CURDATE()
                    THEN 1 ELSE 0
                END
            ) AS today_pending,

            SUM(
                CASE
                    WHEN status = 'Pending'
                    AND MONTH(creation) = MONTH(CURDATE())
                    AND YEAR(creation) = YEAR(CURDATE())
                    THEN 1 ELSE 0
                END
            ) AS month_pending

        FROM `tabField Visits`
        WHERE docstatus < 2
        GROUP BY allocated_to
    """

    return frappe.db.sql(query, as_dict=True)
