# # Copyright (c) 2025, sanprasoftwares@gmail.com and contributors
# # For license information, please see license.txt

# import frappe


# def execute(filters=None):
# 	columns, data = [], []
# 	columns = get_columns(filters)
# 	data = get_data(filters)
# 	return columns, data

# def get_columns(filters):
# 	columns = [
# 		{"label": "User Name","fieldname": "user_name","fieldtype": "Link","options": "User"},
# 		{"label": "Email","fieldname": "email","fieldtype": "Data",},

#         {"label": "Comment", "fieldname": "comment_count", "fieldtype": "Int"},
		
# 		{"label": "Opportunities", "fieldname": "opportunity_count", "fieldtype": "Int"},
#         # {"label": "Opportunities Total", "fieldname": "opportunities_count", "fieldtype": "Int"},
        
# 		{"label": "Quotations", "fieldname": "quotation_count", "fieldtype": "Int"},
#         {"label": "Quotation Total", "fieldname": "quotation_total", "fieldtype": "Currency"},
		
# 		{"label": "Sales Orders", "fieldname": "sales_order_count", "fieldtype": "Int"},
#         {"label": "Sales Order Total", "fieldname": "sales_order_total", "fieldtype": "Currency"},
# 	]
# 	return columns

# def get_data(filters):
	  
# 	user_filter = {
# 		"enabled": 1
# 	} 
# 	if filters and filters.get("user_name"):
# 		user_filter["name"] = filters.get("user_name")

	
# 	from_date = filters.get("from_date")
# 	to_date = filters.get("to_date")





# 	data = []
  
# 	all_data = frappe.get_all("User",filters=user_filter, fields=["full_name", "email"])

# 	for user in all_data:
# 		email = user.email  

# 		date_filter = {"creation": ["between", [from_date, to_date]]}
  
# 		# opp_count = frappe.db.count("Opportunity", {"owner": user.email})
# 		opp_docs = frappe.get_all("Opportunity", filters={**{"owner": email}, **date_filter}, fields=["total"])
# 		opp_count = len(opp_docs)
# 		# quo_count = frappe.db.count("Quotation", {"owner": user.email})
# 		# so_count = frappe.db.count("Sales Order", {"owner": user.email})
# 		comm_count = frappe.db.count("Comment", filters={**{"comment_email": email}, **date_filter})
# 		# frappe.throw(str(comm_count))


# 		quo_docs = frappe.get_all("Quotation", filters={**{"owner": email}, **date_filter}, fields=["total"])
# 		quo_count = len(quo_docs)
# 		quo_total = sum(q["total"] for q in quo_docs)

# 		so_docs = frappe.get_all("Sales Order", filters={**{"owner": email}, **date_filter}, fields=["total"])
# 		so_count = len(so_docs)
# 		so_total = sum(q["total"] for q in so_docs)

# 		data.append({
# 			"user_name": user.full_name,
# 			"email": user.email,
# 			"opportunity_count": opp_count,
# 			# "quotation_count": quo_count,
# 			"quotation_count": quo_count,
#             "quotation_total": quo_total,
# 			# "sales_order_count": so_count,
# 			"sales_order_count": so_count,
#             "sales_order_total": so_total,
# 			"comment_count": comm_count,
# 		})
# 	return data



# Copyright (c) 2025, sanprasoftwares@gmail.com and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import get_datetime


def execute(filters=None):
	columns, data = [], []
	columns = get_columns(filters)
	data = get_data(filters)
	return columns, data


def get_columns(filters):
	columns = [
		{"label": "User Name","fieldname": "user_name","fieldtype": "Link","options": "User", "width": 150},
		{"label": "Email","fieldname": "email","fieldtype": "Data", "width": 250},

		{"label": "Comment", "fieldname": "comment_count", "fieldtype": "Int"},
		
		{"label": "Opportunities", "fieldname": "opportunity_count", "fieldtype": "Int"},
		
		{"label": "Quotations", "fieldname": "quotation_count", "fieldtype": "Int"},
		{"label": "Quotation Total", "fieldname": "quotation_total", "fieldtype": "Currency"},
		
		{"label": "Sales Orders", "fieldname": "sales_order_count", "fieldtype": "Int"},
		{"label": "Sales Order Total", "fieldname": "sales_order_total", "fieldtype": "Currency"},
	]
	return columns


def get_data(filters):

	data = []
	# user_filter = {"enabled": 1} 
	# if filters and filters.get("user_name"):
	# 	user_filter["name"] = filters.get("user_name")

	# all_data = frappe.get_all("User", filters=user_filter, fields=["full_name", "email"])
	all_data = frappe.get_all("Employee",{"department":"Sales - P91"},["user_id"])
	# frappe.throw(str(all_data))
	for row in all_data:
		if not row.user_id:
			continue 
		user = frappe.get_value("User",{"name":row.user_id,"enabled":1},["full_name", "email"],as_dict=True)

		if not user:
			continue
			
		# frappe.msgprint(str(user))
		comm_count = frappe.db.count(
			"Comment",
			filters={
				"comment_email": user.email,
				"creation": [
					"between",
					[
						get_datetime(filters.get("from_date") + " 00:00:00"),
						get_datetime(filters.get("to_date") + " 23:59:59"),
					],
				],
				"comment_type": "Comment",
			},
		)

		opp_docs = frappe.get_all("Opportunity", 
			filters={
				"opportunity_owner": user.email,  # or use owner
				"creation": [
					"between",
					[
						get_datetime(filters.get("from_date") + " 00:00:00"),
						get_datetime(filters.get("to_date") + " 23:59:59"),
					],
				],
			},
			fields=["total"])
		opp_count = len(opp_docs)


		quo_docs = frappe.get_all("Quotation", 
			filters={
				"owner": user.email,
				"creation": [
					"between",
					[
						get_datetime(filters.get("from_date") + " 00:00:00"),
						get_datetime(filters.get("to_date") + " 23:59:59"),
					],
				],
			}, 
			fields=["total", "grand_total"])
		quo_count = len(quo_docs)
		# quo_total = sum(q["total"] for q in quo_docs)
		quo_total = sum(q["grand_total"] for q in quo_docs) # Take the grand total



		so_docs = frappe.get_all("Sales Order", 
			filters={
				"owner": user.email,
				"creation": [
					"between",
					[
						get_datetime(filters.get("from_date") + " 00:00:00"),
						get_datetime(filters.get("to_date") + " 23:59:59"),
					],
				],
			}, 
			fields=["total", "grand_total"])
		so_count = len(so_docs)
		so_total = sum(q["grand_total"] for q in so_docs)



		data.append({
			"user_name": user.full_name,
			"email": user.email,
			"comment_count": comm_count,
			"opportunity_count": opp_count,
			"quotation_count": quo_count,
            "quotation_total": quo_total,
			"sales_order_count": so_count,
            "sales_order_total": so_total,
		})
	return data







# def get_data(filters):
# 	user_filter = {"enabled": 1} 
# 	if filters and filters.get("user_name"):
# 		user_filter["name"] = filters.get("user_name")

# 	from_date = filters.get("from_date")
# 	to_date = filters.get("to_date")

# 	# ✅ Convert to full day range
# 	if from_date and to_date:
# 		from_datetime = from_date + " 00:00:00"
# 		to_datetime = to_date + " 23:59:59"
# 	else:
# 		from_datetime = None
# 		to_datetime = None

# 	data = []
# 	all_data = frappe.get_all("User", filters=user_filter, fields=["full_name", "email"])

# 	for user in all_data:
# 		email = user.email  

# 		# Common filter
# 		date_filter = {"creation": ["between", [from_datetime, to_datetime]]} if from_datetime else {}

# 		# Opportunities
# 		opp_docs = frappe.get_all("Opportunity", filters={**{"owner": email}, **date_filter}, fields=["total"])
# 		opp_count = len(opp_docs)

# 		# 🔥 Fixed Comment filter with full-day handling
# 		if from_datetime:
# 			comm_count = frappe.db.count("Comment", filters={
# 				"comment_email": email,
# 				"creation": ["between", [from_datetime, to_datetime]]
# 			})
# 		else:
# 			comm_count = frappe.db.count("Comment", {"comment_email": email})

# 		# Quotations
# 		quo_docs = frappe.get_all("Quotation", filters={**{"owner": email}, **date_filter}, fields=["total"])
# 		quo_count = len(quo_docs)
# 		quo_total = sum(q["total"] for q in quo_docs)

# 		# Sales Orders
# 		so_docs = frappe.get_all("Sales Order", filters={**{"owner": email}, **date_filter}, fields=["total"])
# 		so_count = len(so_docs)
# 		so_total = sum(q["total"] for q in so_docs)

# 		# Append final row
# 		data.append({
# 			"user_name": user.full_name,
# 			"email": user.email,
# 			"opportunity_count": opp_count,  
# 			"quotation_count": quo_count,
# 			"quotation_total": quo_total,
# 			"sales_order_count": so_count,
# 			"sales_order_total": so_total,
# 			"comment_count": comm_count,
# 		})

# 	return data




