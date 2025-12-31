<p>{% set salesPartnerName = frappe.get_doc("Sales Partner", doc.custom_sales_partner_customer) %}</p>

<p>Dear {{salesPartnerName.name}},</p>  

<p>We’ve assigned you a new lead who has expressed interest in getting STEK PPF installed on their vehicle. Please find the lead details below:</p>

<p>Client Name: {{doc.first_name}}</p>

<p>Contact Info: {{doc.mobile_no}} / {{doc.email_id}}</p>

<p>Vehicle Details: {{doc.custom_vehicle_no}} {{doc.custom_vehicle_no}}</p>

<p>Location: {{doc.city}} {{doc.territory}}</p>

<p>Kindly reach out to the client as soon as possible and keep us updated on the progress.</p>

<p>Best regards,
STEK Team</p> 
