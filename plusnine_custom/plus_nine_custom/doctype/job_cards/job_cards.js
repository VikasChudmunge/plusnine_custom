// Copyright (c) 2025, sanprasoftwares@gmail.com and contributors
// For license information, please see license.txt

frappe.ui.form.on("Job Cards", {
	refresh(frm) {  
        frm.add_custom_button(__('Add Vehicle Checklist'), function () {
            frappe.model.with_doctype('Vehicle Checklist Log', function () {
                let customer_doc = frappe.model.get_new_doc('Vehicle Checklist Log');
                customer_doc.delivery_not_id = frm.doc.name;
                customer_doc.vehicle_no = frm.doc.vehicle_details;
                frappe.set_route('Form', 'Vehicle Checklist Log', customer_doc.name);
            });
        },);

        if (!frm.doc.__islocal && frm.doc.status !== "In Progress" && frm.doc.status !== "Completed" && frm.doc.status == "Acknowledge") {
            frm.add_custom_button(__('Start'), async function() {
                await frm.set_value('status', 'In Progress');
                await frm.save();
                await frm.reload_doc()
            }).addClass('btn-primary');
        } 
        
        // if (!frm.doc.status) {
        //     frm.add_custom_button(__('Acknowledge'), async function() {
        //         await frm.set_value('status', 'Acknowledge');
        //         await frm.save();
        //         await frm.reload_doc()
        //     }).addClass('btn-success');
        // }
                
                // Add 'Completed' button
                if (frm.doc.status === "In Progress") {
                    frm.add_custom_button(__('Completed'),async function() {
                        await frm.set_value('status', 'Completed');
                        await frm.save();
                        await frm.reload_doc()
            }).addClass('btn-success');
        }
        frm.add_custom_button(__('Make Payment'), function () {
            make_payment_entry_from_job_card(frm);
        },);
	},
    // after_save: function(frm) {
    //     if (frm.doc.customer) {
    //         frappe.db.get_value("Customer", frm.doc.customer, "custom_installer")
    //             .then(r => {
    //                 if (r && r.message) {
    //                     // frappe.throw(r.message.custom_installer);
    //                     frappe.db.set_value("Job Cards", frm.doc.name, "installer", r.message.custom_installer);
    //                 }
    //             })
    //     }
    // },
    // after_save: function(frm) {
    //     if (frm.doc.status == "Completed" && frm.doc.document_type == "Sales Order" ) 
    //     {
    //         frappe.db.set_value("Sales Order", frm.doc.document_id, "custom_job_cards", frm.doc.name);
    //     }
    //     else if (frm.doc.status == "Completed" && frm.doc.document_type == "Delivery Note") 
    //     {
    //         frappe.db.set_value("Delivery Note", frm.doc.document_id, "custom_job_card", frm.doc.name);
    //     }
    // },
    // before_delete: function(frm) {
    //     if (frm.doc.status == "Completed" && frm.doc.document_type == "Sales Order" ) 
    //     {
    //         frappe.db.set_value("Sales Order", frm.doc.document_id, "custom_job_cards", '');
    //     }
    //     else if (frm.doc.status == "Completed" && frm.doc.document_type == "Delivery Note") 
    //     {
    //         frappe.db.set_value("Delivery Note", frm.doc.document_id, "custom_job_card", '');
    //     }
    // }
});

function set_job_card_reference(pay_doc, job_card) {
    pay_doc.custom_job_cards = job_card.name;
    const job_card_note = `Job Card: ${job_card.name}`;
    pay_doc.remarks = pay_doc.remarks ? `${pay_doc.remarks}\n${job_card_note}` : job_card_note;
}

function route_to_payment_entry(pay_doc) {
    frappe.model.sync(pay_doc);
    frappe.set_route('Form', 'Payment Entry', pay_doc.name);
}

function make_basic_payment_entry_from_job_card(frm) {
    frappe.model.with_doctype('Payment Entry', function () {
        let pay_doc = frappe.model.get_new_doc('Payment Entry');
        pay_doc.payment_type = 'Receive';
        pay_doc.party_type = 'Customer';
        pay_doc.party = frm.doc.customer;
        pay_doc.party_name = frm.doc.customer_name;
        pay_doc.posting_date = frappe.datetime.get_today();

        set_job_card_reference(pay_doc, frm.doc);
        frappe.model.set_value(pay_doc.doctype, pay_doc.name, 'party', frm.doc.customer);
        route_to_payment_entry(pay_doc);
    });
}

function make_payment_entry_from_job_card(frm) {
    if (!frm.doc.customer) {
        frappe.throw(__('Customer is required to make Payment Entry.'));
    }

    if (frm.doc.document_type === 'Sales Order' && frm.doc.document_id) {
        frappe.call({
            method: 'erpnext.accounts.doctype.payment_entry.payment_entry.get_payment_entry',
            args: {
                dt: frm.doc.document_type,
                dn: frm.doc.document_id
            },
            callback: function(r) {
                if (!r.message) {
                    make_basic_payment_entry_from_job_card(frm);
                    return;
                }

                const pay_doc = r.message;
                set_job_card_reference(pay_doc, frm.doc);
                route_to_payment_entry(pay_doc);
            }
        });
        return;
    }

    make_basic_payment_entry_from_job_card(frm);
}

