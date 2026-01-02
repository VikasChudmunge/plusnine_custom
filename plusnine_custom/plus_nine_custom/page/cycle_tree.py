import frappe
from frappe import _


@frappe.whitelist()
def get_cycle_tree(parent, is_root=False, cycle=None, stage=None):
	if not cycle:
		return []

	if cycle == "sales":
		return _get_sales_tree(parent, is_root, stage)

	if cycle == "purchase":
		return _get_purchase_tree(parent, is_root, stage)

	return []


def _get_sales_tree(parent, is_root, stage=None):
	if is_root:
		stage = stage or "sales_order"
		if stage == "sales_order":
			return _get_all_docs(
				"Sales Order",
				value_prefix="sales_order",
				party_field="customer",
				date_field="transaction_date",
				expandable=True,
			)
		if stage == "delivery_note":
			return _get_all_docs(
				"Delivery Note",
				value_prefix="delivery_note",
				party_field="customer",
				date_field="posting_date",
				expandable=True,
			)
		if stage == "sales_invoice":
			return _get_all_docs(
				"Sales Invoice",
				value_prefix="sales_invoice",
				party_field="customer",
				date_field="posting_date",
				expandable=True,
			)
		if stage == "payment_entry":
			return _get_all_docs(
				"Payment Entry",
				value_prefix="payment_entry",
				party_field="party",
				date_field="posting_date",
				expandable=False,
			)
		return []

	if parent.startswith("sales_order::"):
		sales_order = parent.split("::", 1)[1]
		return [
			_category_node(f"sales_order_delivery_notes::{sales_order}", _("Delivery Notes")),
			_category_node(f"sales_order_sales_invoices::{sales_order}", _("Sales Invoices")),
		]

	if parent.startswith("sales_order_delivery_notes::"):
		sales_order = parent.split("::", 1)[1]
		delivery_notes = _get_child_parents(
			child_doctype="Delivery Note Item",
			link_field="against_sales_order",
			link_value=sales_order,
		)
		return _get_docs_by_name(
			"Delivery Note",
			delivery_notes,
			value_prefix="delivery_note",
			party_field="customer",
			date_field="posting_date",
			expandable=True,
		)

	if parent.startswith("sales_order_sales_invoices::"):
		sales_order = parent.split("::", 1)[1]
		invoices = _get_child_parents(
			child_doctype="Sales Invoice Item",
			link_field="sales_order",
			link_value=sales_order,
		)
		return _get_docs_by_name(
			"Sales Invoice",
			invoices,
			value_prefix="sales_invoice",
			party_field="customer",
			date_field="posting_date",
			expandable=True,
		)

	if parent.startswith("delivery_note::"):
		delivery_note = parent.split("::", 1)[1]
		invoices = _get_child_parents(
			child_doctype="Sales Invoice Item",
			link_field="delivery_note",
			link_value=delivery_note,
		)
		return _get_docs_by_name(
			"Sales Invoice",
			invoices,
			value_prefix="sales_invoice",
			party_field="customer",
			date_field="posting_date",
			expandable=True,
		)

	if parent.startswith("sales_invoice::"):
		sales_invoice = parent.split("::", 1)[1]
		payment_entries = _get_child_parents(
			child_doctype="Payment Entry Reference",
			link_field="reference_name",
			link_value=sales_invoice,
			filters_extra={"reference_doctype": "Sales Invoice"},
		)
		return _get_docs_by_name(
			"Payment Entry",
			payment_entries,
			value_prefix="payment_entry",
			date_field="posting_date",
		)

	return []


def _get_purchase_tree(parent, is_root, stage=None):
	if is_root:
		stage = stage or "material_request"
		if stage == "material_request":
			return _get_all_docs(
				"Material Request",
				value_prefix="material_request",
				party_field="company",
				date_field="transaction_date",
				expandable=True,
				filters_extra={"material_request_type": "Purchase"},
			)
		if stage == "request_for_quotation":
			return _get_all_docs(
				"Request for Quotation",
				value_prefix="request_for_quotation",
				date_field="transaction_date",
				expandable=True,
			)
		if stage == "supplier_quotation":
			return _get_all_docs(
				"Supplier Quotation",
				value_prefix="supplier_quotation",
				party_field="supplier",
				date_field="transaction_date",
				expandable=True,
			)
		if stage == "purchase_order":
			return _get_all_docs(
				"Purchase Order",
				value_prefix="purchase_order",
				party_field="supplier",
				date_field="transaction_date",
				expandable=True,
			)
		if stage == "purchase_receipt":
			return _get_all_docs(
				"Purchase Receipt",
				value_prefix="purchase_receipt",
				party_field="supplier",
				date_field="posting_date",
				expandable=True,
			)
		if stage == "purchase_invoice":
			return _get_all_docs(
				"Purchase Invoice",
				value_prefix="purchase_invoice",
				party_field="supplier",
				date_field="posting_date",
				expandable=True,
			)
		if stage == "payment_entry":
			return _get_all_docs(
				"Payment Entry",
				value_prefix="payment_entry",
				party_field="party",
				date_field="posting_date",
				expandable=False,
			)
		return []

	if parent.startswith("material_request::"):
		material_request = parent.split("::", 1)[1]
		rfqs = _get_child_parents(
			child_doctype="Request for Quotation Item",
			link_field="material_request",
			link_value=material_request,
		)
		return _get_docs_by_name(
			"Request for Quotation",
			rfqs,
			value_prefix="request_for_quotation",
			date_field="transaction_date",
			expandable=True,
		)

	if parent.startswith("request_for_quotation::"):
		rfq = parent.split("::", 1)[1]
		supplier_quotations = _get_child_parents(
			child_doctype="Supplier Quotation Item",
			link_field="request_for_quotation",
			link_value=rfq,
		)
		return _get_docs_by_name(
			"Supplier Quotation",
			supplier_quotations,
			value_prefix="supplier_quotation",
			party_field="supplier",
			date_field="transaction_date",
			expandable=True,
		)

	if parent.startswith("supplier_quotation::"):
		supplier_quotation = parent.split("::", 1)[1]
		purchase_orders = _get_child_parents(
			child_doctype="Purchase Order Item",
			link_field="supplier_quotation",
			link_value=supplier_quotation,
		)
		return _get_docs_by_name(
			"Purchase Order",
			purchase_orders,
			value_prefix="purchase_order",
			party_field="supplier",
			date_field="transaction_date",
			expandable=True,
		)

	if parent.startswith("purchase_order::"):
		purchase_order = parent.split("::", 1)[1]
		purchase_receipts = _get_child_parents(
			child_doctype="Purchase Receipt Item",
			link_field="purchase_order",
			link_value=purchase_order,
		)
		return _get_docs_by_name(
			"Purchase Receipt",
			purchase_receipts,
			value_prefix="purchase_receipt",
			party_field="supplier",
			date_field="posting_date",
			expandable=True,
		)

	if parent.startswith("purchase_receipt::"):
		purchase_receipt = parent.split("::", 1)[1]
		purchase_invoices = _get_child_parents(
			child_doctype="Purchase Invoice Item",
			link_field="purchase_receipt",
			link_value=purchase_receipt,
		)
		return _get_docs_by_name(
			"Purchase Invoice",
			purchase_invoices,
			value_prefix="purchase_invoice",
			party_field="supplier",
			date_field="posting_date",
			expandable=True,
		)

	if parent.startswith("purchase_invoice::"):
		purchase_invoice = parent.split("::", 1)[1]
		payment_entries = _get_child_parents(
			child_doctype="Payment Entry Reference",
			link_field="reference_name",
			link_value=purchase_invoice,
			filters_extra={"reference_doctype": "Purchase Invoice"},
		)
		return _get_docs_by_name(
			"Payment Entry",
			payment_entries,
			value_prefix="payment_entry",
			date_field="posting_date",
		)

	return []


def _category_node(value, label):
	return {
		"value": value,
		"display_label": label,
		"expandable": True,
	}


def _get_all_docs(
	doctype, value_prefix, party_field=None, date_field=None, expandable=False, filters_extra=None
):
	filters = {"docstatus": ("<", 2)}
	if filters_extra:
		filters.update(filters_extra)
	fields = ["name"]

	if party_field:
		fields.append(party_field)

	order_by = None
	if date_field:
		order_by = f"{date_field} desc"

	docs = frappe.get_list(doctype, filters=filters, fields=fields, order_by=order_by, limit_page_length=0)
	return _make_doc_nodes(doctype, docs, value_prefix, party_field, expandable=expandable)


def _get_docs_by_name(
	doctype, names, value_prefix, party_field=None, date_field=None, expandable=False
):
	if not names:
		return [_empty_node(value_prefix)]

	fields = ["name"]
	if party_field:
		fields.append(party_field)

	order_by = None
	if date_field:
		order_by = f"{date_field} desc"

	docs = frappe.get_list(
		doctype,
		filters={"name": ("in", names), "docstatus": ("<", 2)},
		fields=fields,
		order_by=order_by,
		limit_page_length=0,
	)
	return _make_doc_nodes(doctype, docs, value_prefix, party_field, expandable=expandable)


def _get_child_parents(child_doctype, link_field, link_value, filters_extra=None):
	item = frappe.qb.DocType(child_doctype)
	query = frappe.qb.from_(item).select(item.parent).where(item[link_field] == link_value)
	if frappe.get_meta(child_doctype).has_field("docstatus"):
		query = query.where(item.docstatus < 2)
	if filters_extra:
		for fieldname, value in filters_extra.items():
			query = query.where(item[fieldname] == value)

	rows = query.groupby(item.parent).run(as_dict=True)
	return [row.parent for row in rows]


def _make_doc_nodes(doctype, docs, value_prefix, party_field=None, expandable=False):
	if not docs:
		return [_empty_node(value_prefix)]

	nodes = []
	for doc in docs:
		name = doc.get("name")
		party = doc.get(party_field) if party_field else None
		display = f"{name} - {party}" if party else name

		node = {
			"value": f"{value_prefix}::{name}",
			"display_label": display,
			"expandable": expandable,
		}

		if not expandable:
			node["route"] = ["Form", doctype, name]

		nodes.append(node)

	return nodes


def _empty_node(prefix):
	return {
		"value": f"empty::{prefix}::{frappe.generate_hash(length=6)}",
		"display_label": _("No records found"),
		"expandable": False,
	}
