from erpnext.controllers.taxes_and_totals import get_itemised_tax
import frappe
from frappe.utils.data import cint

def get_invoice_item_and_tax_details(voucher_type, voucher_no, hsn_wise = False):
    doc = frappe.get_doc(voucher_type, voucher_no)
    itemised_tax = get_itemised_tax(doc.taxes)
    items = doc.items
    instate = False
    total_cgst, total_sgst, total_igst = 0, 0, 0
    tax_details = {}
    for row in items:
        if row.item_code in itemised_tax:
            cgst, sgst, igst = 0, 0, 0
            for tax in itemised_tax.get(row.item_code):
                
                if 'cgst' in (tax or '').lower():
                    instate = True
                    row.cgst = itemised_tax.get(row.item_code).get(tax).get('tax_rate') or 0
                    row.cgst_percent = f"{cint(row.cgst) if cint(row.cgst)==row.cgst else row.cgst}%"
                    cgst += row.amount * row.cgst / 100

                elif 'sgst' in (tax or '').lower():
                    instate = True
                    row.sgst = itemised_tax.get(row.item_code).get(tax).get('tax_rate') or 0
                    row.sgst_percent = f"{cint(row.sgst) if cint(row.sgst)==row.sgst else row.sgst}%"
                    sgst += row.amount * row.sgst / 100

                elif 'igst' in (tax or '').lower():
                    instate = False
                    row.igst = itemised_tax.get(row.item_code).get(tax).get('tax_rate') or 0
                    row.igst_percent = f"{cint(row.igst) if cint(row.igst)==row.igst else row.igst}%"
                    igst += row.amount * row.igst / 100
                
            row.cgst_amount = cgst
            row.sgst_amount = sgst
            row.igst_amount = igst

            tax_percent = f"{(row.get('cgst') or 0) + (row.get('sgst') or 0) + (row.get('igst') or 0)} {row.gst_hsn_code if hsn_wise else ''}" 
            if tax_percent not in tax_details:
                tax_details[tax_percent] = {
                    'gst_hsn_code': row.gst_hsn_code,
                    'tax_percentage': ((row.get('cgst') or 0) + (row.get('sgst') or 0))/ 2+ (row.get('igst') or 0),
                    'tax_percentage_so': (row.get('cgst') or 0) + (row.get('sgst') or 0)+ (row.get('igst') or 0),
                    'taxable_amount': row.net_amount or 0,
                    'cgst': cgst,
                    'sgst': sgst,
                    'igst': igst,
                    'total_tax_amount': (cgst or 0) + (sgst or 0) + (igst or 0)
                }
            else:
                tax_details[tax_percent]['taxable_amount'] += row.net_amount or 0
                tax_details[tax_percent]['cgst'] += cgst
                tax_details[tax_percent]['sgst'] += sgst
                tax_details[tax_percent]['igst'] += igst
                tax_details[tax_percent]['total_tax_amount'] += (cgst or 0) + (sgst or 0) + (igst or 0)

            total_cgst += cgst
            total_sgst += sgst
            total_igst += igst
    frieght_amount=0
    frieght_tax=0
    if voucher_type == "Sales Order":
        for freight in doc.taxes :
            if "Freight" in  freight.description :
                frieght_amount=freight.tax_amount
                frieght_tax=frieght_amount*(18/100)
            
    total=[] 
    if voucher_type == "Sales Order":
          total.append({
            'tax_percentage_so':'Frieght',
            'taxable_amount': frieght_amount,
            'cgst': frieght_tax/2,
            'sgst': frieght_tax/2,
            'igst': frieght_tax,
            'total_tax_amount': frieght_tax
        })
    total.append({
            'tax_percentage': 'Totals',
            'tax_percentage_so':'Totals',
            'taxable_amount': doc.net_total,
            'cgst': total_cgst,
            'sgst': total_sgst,
            'igst': total_igst,
            'total_tax_amount': (total_cgst or 0) + (total_sgst or 0) + (total_igst or 0)
        })
    return {
        "items": items,
        "instate": instate,
        "tax_details": list(tax_details.values()) + total,
        "cgst": total_cgst,
        "sgst": total_sgst,
        "igst": total_igst,
    }