# import frappe
# from frappe.utils import nowdate


# def execute(filters=None):
#     columns = get_columns()
#     data = get_data()
#     return columns, data


# def get_columns():
#     return [
#         {
#             "label": "Campaign",
#             "fieldname": "campaign",
#             "fieldtype": "Link",
# 			"options": "Campaign",
#             "width": 200
#         },
#         {
#             "label": "Total Leads",
#             "fieldname": "total_leads",
#             "fieldtype": "Int",
#             "width": 120
#         },
#         {
#             "label": "Contacted Today",
#             "fieldname": "contacted_today",
#             "fieldtype": "Int",
#             "width": 140
#         },
#         {
#             "label": "Pending Contact",
#             "fieldname": "pending_contact",
#             "fieldtype": "Int",
#             "width": 140
#         },
#         {
#             "label": "Interested Count",
#             "fieldname": "interested_count",
#             "fieldtype": "Int",
#             "width": 150
#         }
#     ]


# def get_data():
#     data = {}

#     # -----------------------------
#     # 1️⃣ Total Leads (Campaign wise)
#     # -----------------------------
#     total_leads = frappe.db.sql("""
#         SELECT
#             campaign_name,
#             COUNT(name) AS total
#         FROM `tabLead`
#         WHERE campaign_name IS NOT NULL AND campaign_name != ''
#         GROUP BY campaign_name
#     """, as_dict=True)

#     for row in total_leads:
#         data[row.campaign_name] = {
#             "campaign": row.campaign_name,
#             "total_leads": row.total,
#             "contacted_today": 0,
#             "pending_contact": 0,
#             "interested_count": 0
#         }

#     # -----------------------------
#     # 2️⃣ Contacted Today
#     # Status != Open OR Comment Added Today
#     # -----------------------------
#     contacted_today = frappe.db.sql("""
#         SELECT
#             l.campaign_name,
#             COUNT(DISTINCT l.name) AS cnt
#         FROM `tabLead` l
#         LEFT JOIN `tabComment` c
#             ON c.reference_doctype = 'Lead'
#             AND c.reference_name = l.name
#         WHERE
#             l.campaign_name IS NOT NULL
#             AND (
#                 (DATE(l.modified) = CURDATE() AND l.status != 'Open')
#                 OR DATE(c.creation) = CURDATE()
#             )
#         GROUP BY l.campaign_name
#     """, as_dict=True)

#     for row in contacted_today:
#         if row.campaign_name in data:
#             data[row.campaign_name]["contacted_today"] = row.cnt

#     # -----------------------------
#     # 3️⃣ Pending Contact (Open)
#     # -----------------------------
#     pending_contact = frappe.db.sql("""
#         SELECT
#             campaign_name,
#             COUNT(name) AS cnt
#         FROM `tabLead`
#         WHERE
#             status IN (
# 			'Open',
# 			"Not Interested"
# 			)
#             AND campaign_name IS NOT NULL
#         GROUP BY campaign_name
#     """, as_dict=True)

#     for row in pending_contact:
#         if row.campaign_name in data:
#             data[row.campaign_name]["pending_contact"] = row.cnt

#     # -----------------------------
#     # 4️⃣ Interested Count
#     # Lead OR Opportunity OR Quotation OR Prospect
#     # -----------------------------
#     interested = frappe.db.sql("""
#         SELECT campaign_name, COUNT(name) cnt
#         FROM `tabLead`
#         WHERE
#             campaign_name IS NOT NULL
#             AND status IN (
#                 'Interested',
#                 'Lead',
#                 'Quotation',
#                 'Opportunity',
#                 'Prospect'
#             )
#         GROUP BY campaign_name
#     """, as_dict=True)

#     for row in interested:
#         if row.campaign_name in data:
#             data[row.campaign_name]["interested_count"] = row.cnt

#     return list(data.values())



import frappe


def execute(filters=None): 
    columns = get_columns()
    data = get_data()
    return columns, data


def get_columns():
    return [
        {"label": "Campaign", "fieldname": "campaign", "fieldtype": "Data", "width": 200},
        {"label": "Today Created", "fieldname": "today_created", "fieldtype": "Int", "width": 130},
        {"label": "Today Lead Nurture", "fieldname": "today_lead_nudshet", "fieldtype": "Int", "width": 170},
        {"label": "Total Leads", "fieldname": "total_leads", "fieldtype": "Int", "width": 120},
        {"label": "Contacted Today", "fieldname": "contacted_today", "fieldtype": "Int", "width": 140},
        {"label": "Pending Contact", "fieldname": "pending_contact", "fieldtype": "Int", "width": 140},
        {"label": "Interested Count", "fieldname": "interested_count", "fieldtype": "Int", "width": 150},
    ]


def get_data():
    data = {}

    # -----------------------------
    # 1️⃣ Total Leads (Include Not Set)
    # -----------------------------
    total_leads = frappe.db.sql("""
        SELECT
            IFNULL(NULLIF(campaign_name, ''), 'Not Set') AS campaign,
            COUNT(name) AS total
        FROM `tabLead`
        GROUP BY campaign
    """, as_dict=True)

    for row in total_leads:
        data[row.campaign] = {
            "campaign": row.campaign,
            "today_created": 0,
            "today_lead_nudshet": 0,
            "total_leads": row.total,
            "contacted_today": 0,
            "pending_contact": 0,
            "interested_count": 0
        }

    # -----------------------------
    # 2️⃣ Today Created Leads
    # -----------------------------
    today_created = frappe.db.sql("""
        SELECT
            IFNULL(NULLIF(campaign_name, ''), 'Not Set') AS campaign,
            COUNT(name) AS cnt
        FROM `tabLead`
        WHERE DATE(creation) = CURDATE()
        GROUP BY campaign
    """, as_dict=True)

    for row in today_created:
        if row.campaign in data:
            data[row.campaign]["today_created"] = row.cnt

    # -----------------------------
    # 3️⃣ Contacted Today (Any update, not by Administrator)
    # -----------------------------
    contacted_today = frappe.db.sql("""
        SELECT
            IFNULL(NULLIF(campaign_name, ''), 'Not Set') AS campaign,
            COUNT(name) AS cnt
        FROM `tabLead`
        WHERE
            DATE(modified) = CURDATE()
            AND modified_by != 'Administrator'
        GROUP BY campaign
    """, as_dict=True)

    for row in contacted_today:
        if row.campaign in data:
            data[row.campaign]["contacted_today"] = row.cnt

    # -----------------------------
    # 4️⃣ Today Lead Nudshet
    # (Created today + Qualified statuses)
    # -----------------------------
    today_lead_nudshet = frappe.db.sql("""
        SELECT
            IFNULL(NULLIF(campaign_name, ''), 'Not Set') AS campaign,
            COUNT(name) AS cnt
        FROM `tabLead`
        WHERE
            DATE(creation) = CURDATE()
            AND status IN (
                'Quotation',
                'Opportunity',
                'Interested',
                'Converted'
            )
        GROUP BY campaign
    """, as_dict=True)

    for row in today_lead_nudshet:
        if row.campaign in data:
            data[row.campaign]["today_lead_nudshet"] = row.cnt

    # -----------------------------
    # 5️⃣ Pending Contact
    # -----------------------------
    pending_contact = frappe.db.sql("""
        SELECT
            IFNULL(NULLIF(campaign_name, ''), 'Not Set') AS campaign,
            COUNT(name) AS cnt
        FROM `tabLead`
        WHERE status IN ('Open', 'Lead')
        GROUP BY campaign
    """, as_dict=True)

    for row in pending_contact:
        if row.campaign in data:
            data[row.campaign]["pending_contact"] = row.cnt

    # -----------------------------
    # 6️⃣ Interested Count (Status Based)
    # -----------------------------
    interested = frappe.db.sql("""
        SELECT
            IFNULL(NULLIF(campaign_name, ''), 'Not Set') AS campaign,
            COUNT(name) AS cnt
        FROM `tabLead`
        WHERE status IN (
            'Interested',
            'Lead',
            'Quotation',
            'Opportunity',
            'Prospect'
        )
        GROUP BY campaign
    """, as_dict=True)

    for row in interested:
        if row.campaign in data:
            data[row.campaign]["interested_count"] = row.cnt

    return list(data.values())
