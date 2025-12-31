# import frappe
# from frappe.utils.pdf import get_pdf
# from frappe.utils import get_url

# def create_and_attach_pdf(doc, method):

#     # Generate PDF
#     pdf_content = get_pdf(frappe.get_print(doc.doctype, doc.name, print_format="TS Sales Invoice"))

#     # Check if a file with the same name is already attached
#     existing_file = frappe.get_all(
#         "File",
#         filters={
#             "attached_to_doctype": doc.doctype,
#             "attached_to_name": doc.name,
#             "file_name": f"{doc.name}.pdf"
#         },
#         limit=1
#     )

#     if existing_file:
#         # Update existing file
#         filedoc = frappe.get_doc("File", existing_file[0].name)
#         filedoc.content = pdf_content
#         filedoc.save(ignore_permissions=True)
#     else:
#         # Create new file if none exists
#         filedoc = frappe.get_doc({
#             "doctype": "File",
#             "file_name": f"{doc.name}.pdf",
#             "attached_to_doctype": doc.doctype,
#             "attached_to_name": doc.name,
#             "is_private": 0,
#             "content": pdf_content,
#             "decode": False
#         })
#         # filedoc.save(ignore_permissions=True)
#         filedoc = save_file(file_name,pdf_content,doc.doctype,doc.name,is_private=0)

#     # Get public URL
#     public_url = get_url(filedoc.file_url)

#     # Update the custom field with latest PDF link
#     frappe.db.set_value(doc.doctype, doc.name, "custom_pdf_link", public_url)
#     doc.load_from_db()

#     frappe.msgprint(f"PDF Generated/Updated: <a href='{public_url}' target='_blank'>{public_url}</a>")


# import frappe
# from frappe.utils.pdf import get_pdf
# from frappe.utils import get_url
# from frappe.utils.file_manager import save_file

# def create_and_attach_pdf(doc, method):
#     """
#     Generate or update PDF for a Sales Invoice and attach it to the record.
#     Updates custom_pdf_link with the latest URL.
#     """
#     # Generate fresh PDF
#     pdf_content = get_pdf(
#         frappe.get_print(doc.doctype, doc.name, print_format="TS Sales Invoice")
#     )

#     file_name = f"{doc.name}.pdf"

#     # Check if already exists
#     existing_file = frappe.get_all(
#         "File",
#         filters={
#             "attached_to_doctype": doc.doctype,
#             "attached_to_name": doc.name,
#             "file_name": file_name,
#         },
#         limit=1,
#     )

#     if existing_file:
#         # Delete old file (simplest way to ensure refresh)
#         frappe.delete_doc("File", existing_file[0].name, ignore_permissions=True)

#     # Save new file
#     filedoc = save_file(
#         file_name,
#         pdf_content,
#         doc.doctype,
#         doc.name,
#         is_private=0
#     )

#     # Get public URL
#     public_url = get_url(filedoc.file_url)

#     # Update custom field with link
#     frappe.db.set_value(doc.doctype, doc.name, "custom_pdf_link", public_url)
#     doc.reload()

#     frappe.msgprint(
#         f"PDF Generated/Updated: <a href='{public_url}' target='_blank'>{public_url}</a>"
#     )

  
# import frappe
# from frappe.utils.pdf import get_pdf
# from frappe.utils import get_url
# from frappe.utils.file_manager import save_file_on_filesystem

# @frappe.whitelist()
# def create_and_attach_pdf(doc): 
#     # Generate fresh PDF
#     pdf_content = get_pdf(  
#         frappe.get_print(doc.doctype, doc.name, print_format="TS Sales Invoice")
#     )

#     file_name = f"{doc.name}.pdf"

#     # Check if already exists
#     existing_file = frappe.get_all(
#         "File",
#         filters={
#             "attached_to_doctype": doc.doctype,
#             "attached_to_name": doc.name,
#             "file_name": file_name,
#         },
#         limit=1,
#     )

#     if existing_file:
#         # Update the existing file
#         filedoc = frappe.get_doc("File", existing_file[0].name)
#         filedoc.content = pdf_content
#         filedoc.decode = False   # Important, ensures raw content is used
#         save_file_on_filesystem(filedoc)  # Overwrites the file on disk
#         filedoc.save(ignore_permissions=True)
#     else:
#         # Create new file if none exists
#         filedoc = frappe.get_doc({
#             "doctype": "File",
#             "file_name": file_name,
#             "attached_to_doctype": doc.doctype,
#             "attached_to_name": doc.name,
#             "is_private": 0, 
#             "content": pdf_content,
#             "decode": False
#         })
#         filedoc.save(ignore_permissions=True)

#     # Get public URL
#     public_url = get_url(filedoc.file_url)

#     # Update custom field with link
#     frappe.db.set_value(doc.doctype, doc.name, "custom_pdf_link", public_url)
#     doc.reload()

#     frappe.msgprint(
#         f"PDF Generated/Updated: <a href='{public_url}' target='_blank'>{public_url}</a>"
#     )

import frappe
from frappe.utils.pdf import get_pdf
from frappe.utils import get_url
from frappe.utils.file_manager import save_file

@frappe.whitelist()
def create_and_attach_pdf(doctype, docname): 
    doc = frappe.get_doc(doctype, docname)

    pdf_content = get_pdf(
        frappe.get_print(doctype, docname, print_format="TS Sales Invoice")
    )

    file_name = f"{docname}.pdf"

    # Save or update file
    filedoc = save_file(file_name, pdf_content, doctype, docname, is_private=0)

    public_url = get_url(filedoc.file_url)

    frappe.db.set_value(doctype, docname, "custom_pdf_link", public_url)

    return public_url




# Send PDF with attechments.....................................................................................

# import frappe
# from frappe.utils.pdf import get_pdf
# from frappe.core.doctype.communication.email import make

# def send_invoice_email(doc, method):

#     # 1️⃣ Sales Invoice PDF
#     html = frappe.get_print("Sales Invoice", doc.name, print_format="TS Sales Invoice")
#     sales_invoice_pdf = get_pdf(html)

#     attachments = [
#         {
#             "fname": f"{doc.name}.pdf",
#             "fcontent": sales_invoice_pdf
#         }
#     ]

#     # 2️⃣ Attach Item-wise custom PDF from child table
#     for row in doc.items:
#         if row.item_code:

#             # fetch custom attachment file from Item
#             custom_file = frappe.db.get_value(
#                 "Item",
#                 row.item_code,
#                 "custom_attach"
#             )

#             if custom_file:
#                 try:
#                     file_doc = frappe.get_doc("File", {"file_url": custom_file})
#                     file_content = file_doc.get_content()

#                     attachments.append({
#                         "fname": file_doc.file_name,
#                         "fcontent": file_content
#                     })

#                 except Exception as e:
#                     frappe.log_error(f"Could not attach file for item {row.item_code}: {e}")

#     # 3️⃣ Get recipient email
#     recipient_email = doc.contact_email or doc.customer_email_id or None
#     if not recipient_email:
#         frappe.log_error("Sales Invoice Email Failed: No Email in Customer or Contact")
#         return

#     # 4️⃣ Send Email
#     make(
#         recipients=[recipient_email],
#         subject=f"Sales Invoice {doc.name}",
#         content="Please find your invoice and related attachments.",
#         attachments=attachments,
#         send_email=True
#     )



import frappe
from frappe.utils.pdf import get_pdf
from frappe.core.doctype.communication.email import make

def send_invoice_email(doc, method):

    # 1️⃣ Generate Sales Invoice PDF
    html = frappe.get_print("Sales Invoice", doc.name, print_format="TS Sales Invoice")
    sales_invoice_pdf = get_pdf(html)

    attachments = [
        {
            "fname": f"{doc.name}.pdf",
            "fcontent": sales_invoice_pdf
        }
    ]

    # 2️⃣ Attach Item-wise custom PDF
    for row in doc.items:
        if row.item_code:
            custom_file = frappe.db.get_value("Item", row.item_code, "custom_attach")

            if custom_file:
                try:
                    file_doc = frappe.get_doc("File", {"file_url": custom_file})
                    file_content = file_doc.get_content()

                    attachments.append({
                        "fname": file_doc.file_name,
                        "fcontent": file_content
                    })

                except Exception as e:
                    frappe.log_error(f"Could not attach file for item {row.item_code}: {e}")

    # 3️⃣ Recipient Email
    recipient_email = doc.contact_email or doc.customer_email_id or None
    if not recipient_email:
        frappe.log_error("Sales Invoice Email Failed: No Email in Customer or Contact")
        return

    # 4️⃣ Build Custom HTML Body (Replace variables)
    customer_person = doc.contact_person or doc.customer or "Customer"

    email_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>New Sales Invoice Raised</title>
    </head>
    <body>
        <p>Dear {customer_person},</p>
        <p>Your Sales Invoice has been created. 
        Please check the attached PDF for full details.</p>
    
        <p>Thank you.</p>
    </body>
    </html>
    """

    # 5️⃣ Send Email
    make(
        recipients=[recipient_email],
        subject=f"Sales Invoice {doc.name}",
        content=email_html,
        attachments=attachments,
        send_email=True,
        is_html=True
    )
