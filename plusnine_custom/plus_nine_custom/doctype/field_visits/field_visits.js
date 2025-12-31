// Copyright (c) 2025, sanprasoftwares@gmail.com and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Field Visits", {
// 	refresh(frm) {

// 	},
// });
 // Copyright (c) 2025, sanprasoftwares@gmail.com and contributors
// For license information, please see license.txt


frappe.ui.form.on("Field Visits", { 
	refresh(frm) {
        frm.set_intro("Please Save Doc to attach files") 
	},
    start_time: function(frm) {
        if(!frm.doc.start){
            frm.doc.start = frappe.datetime.now_datetime();
            frm.doc.status = "Started"
            // frm.doc.refresh_field("items");
            frm.dirty()
            frm.save();   
        }
    },
    end_time: function(frm) {

        if (!frm.doc.end) {
            frm.doc.end = frappe.datetime.now_datetime();
        }

        // calculate span if start and end exist
        if (frm.doc.start && frm.doc.end) {
            let start_time = frappe.datetime.str_to_obj(frm.doc.start);
            let end_time = frappe.datetime.str_to_obj(frm.doc.end);

            // difference in seconds
            let diff_in_seconds = Math.floor((end_time - start_time) / 1000);

            if (diff_in_seconds > 0) {
                let hours = Math.floor(diff_in_seconds / 3600);
                let minutes = Math.floor((diff_in_seconds % 3600) / 60);
                let seconds = diff_in_seconds % 60;

                // format result like "1 Hour 30 Minutes 20 Seconds"
                let result = "";
                if (hours > 0) result += hours + " Hour" + (hours > 1 ? "s " : " ");
                if (minutes > 0) result += minutes + " Minute" + (minutes > 1 ? "s " : " ");
                if (seconds > 0) result += seconds + " Second" + (seconds > 1 ? "s" : "");

                frm.doc.status = "Completed" 
                frm.doc.meeting_span = result.trim();
            } else {
                frm.doc.meeting_span = "0 Seconds";
            }
            // frm.refresh_field("items"); 
            frm.dirty();
            frm.save();
        }
    },
    attach_files(frm){
        if(frm.is_new()){    
            frappe.throw("First Save the Form to attach Documents")
            return
        }
    }
});

// frappe.ui.form.on("Field Visit Items", {
//     start_time: function(frm, cdt, cdn) {
//         let row = locals[cdt][cdn]
//         if(!row.start){
//             row.start = frappe.datetime.now_datetime();
//             row.status = "Started"
//             frm.refresh_field("items");
//             frm.dirty()
//             frm.save();   
//         }
//     },
//     end_time: function(frm, cdt, cdn) {
//     let row = locals[cdt][cdn];

//     // if no end, set current datetime
//     if (!row.end) {
//         row.end = frappe.datetime.now_datetime();
//     }

//     // calculate span if start and end exist
//     if (row.start && row.end) {
//         let start_time = frappe.datetime.str_to_obj(row.start);
//         let end_time = frappe.datetime.str_to_obj(row.end);

//         // difference in seconds
//         let diff_in_seconds = Math.floor((end_time - start_time) / 1000);

//         if (diff_in_seconds > 0) {
//             let hours = Math.floor(diff_in_seconds / 3600);
//             let minutes = Math.floor((diff_in_seconds % 3600) / 60);
//             let seconds = diff_in_seconds % 60;

//             // format result like "1 Hour 30 Minutes 20 Seconds"
//             let result = "";
//             if (hours > 0) result += hours + " Hour" + (hours > 1 ? "s " : " ");
//             if (minutes > 0) result += minutes + " Minute" + (minutes > 1 ? "s " : " ");
//             if (seconds > 0) result += seconds + " Second" + (seconds > 1 ? "s" : "");

//             row.status = "Completed" 
//             row.meeting_span = result.trim();
//         } else {
//             row.meeting_span = "0 Seconds";
//         }
//         frm.refresh_field("items"); 
//         frm.dirty();
//         frm.save();
//     }
// },
//     attach_files(frm){
//         if(frm.is_new()){    
//             frappe.throw("First Save the Form to attach Documents")
//             return
//         }
//     }
    
// });
