// // Copyright (c) 2025, sanprasoftwares@gmail.com and contributors
// // For license information, please see license.txt

// frappe.query_reports["Camping Wise Lead Report"] = {
// 	"filters": [

// 	],
// 	 onload: function (report) {

//         // Prevent duplicate insertion
//         if (document.getElementById("campaign-wise-lead-doc-table")) {
//             return;
//         }

//         const doc_table = `
//             <div id="campaign-wise-lead-doc-table"
//                 style="
//                     background: #ffffff;
//                     border: 1px solid #d1d8dd;
//                     padding: 15px;
//                     border-radius: 6px;
//                     margin-bottom: 16px;
//                     font-size: 13px;
//                 ">

//                 <b>📘 Campaign Wise Lead Report – Column Description</b>
//                 <br><br>

//                 <table style="
//                     width: 80%;
//                     border-collapse: collapse;
//                     font-size: 13px;
//                 ">
//                     <thead>
//                         <tr style="background:#f5f7fa;">
//                             <th style="border:1px solid #d1d8dd; padding:8px; width:20%;">Column</th>
//                             <th style="border:1px solid #d1d8dd; padding:8px;">Description</th>
//                             <th style="border:1px solid #d1d8dd; padding:8px; width:35%;">Conditions / Status</th>
//                         </tr>
//                     </thead>
//                     <tbody>
//                         <tr>
//                             <td style="border:1px solid #d1d8dd; padding:8px;"><b>Campaign</b></td>
//                             <td style="border:1px solid #d1d8dd; padding:8px;">
//                                 Displays the Campaign Name
//                             </td>
//                             <td style="border:1px solid #d1d8dd; padding:8px;">
//                                 Empty values shown as <b>Not Set</b>
//                             </td>
//                         </tr>

//                         <tr>
//                             <td style="border:1px solid #d1d8dd; padding:8px;"><b>Today Created</b></td>
//                             <td style="border:1px solid #d1d8dd; padding:8px;">
//                                 Number of leads created today
//                             </td>
//                             <td style="border:1px solid #d1d8dd; padding:8px;">
//                                 <code>DATE(creation) = CURDATE()</code>
//                             </td>
//                         </tr>
 
//                         <tr>
//                             <td style="border:1px solid #d1d8dd; padding:8px;"><b>Today Lead Nurture</b></td>
//                             <td style="border:1px solid #d1d8dd; padding:8px;">
//                                 Leads created today with qualified status
//                             </td>
//                             <td style="border:1px solid #d1d8dd; padding:8px;">
//                                 Interested, Quotation, Opportunity, Converted
//                             </td>
//                         </tr>

//                         <tr>
//                             <td style="border:1px solid #d1d8dd; padding:8px;"><b>Total Leads</b></td>
//                             <td style="border:1px solid #d1d8dd; padding:8px;">
//                                 Total number of leads per campaign
//                             </td>
//                             <td style="border:1px solid #d1d8dd; padding:8px;">
//                                 All leads
//                             </td>
//                         </tr>

//                         <tr>
//                             <td style="border:1px solid #d1d8dd; padding:8px;"><b>Contacted Today</b></td>
//                             <td style="border:1px solid #d1d8dd; padding:8px;">
//                                 Leads updated today
//                             </td>
//                             <td style="border:1px solid #d1d8dd; padding:8px;">
//                                 Status change or any update<br>
//                                 Excludes Administrator<br>
//                                 <code>DATE(modified) = CURDATE()</code>
//                             </td>
//                         </tr>

//                         <tr>
//                             <td style="border:1px solid #d1d8dd; padding:8px;"><b>Pending Contact</b></td>
//                             <td style="border:1px solid #d1d8dd; padding:8px;">
//                                 Leads pending follow-up
//                             </td>
//                             <td style="border:1px solid #d1d8dd; padding:8px;">
//                                 Open, Lead
//                             </td>
//                         </tr>

//                         <tr>
//                             <td style="border:1px solid #d1d8dd; padding:8px;"><b>Interested Count</b></td>
//                             <td style="border:1px solid #d1d8dd; padding:8px;">
//                                 Leads showing interest
//                             </td>
//                             <td style="border:1px solid #d1d8dd; padding:8px;">
//                                 Interested, Lead, Quotation, Opportunity, Prospect
//                             </td>
//                         </tr>
//                     </tbody>
//                 </table>
//             </div>
//         `;

//         // Insert documentation table above report grid
//         report.page.main.append(doc_table);
//     }
// };
  


frappe.query_reports["Camping Wise Lead Report"] = {
    "filters": [],

    onload: function (report) {

        // 🔹 Remove existing table if already added
        $("#campaign-wise-lead-doc-table").remove();

        const doc_table = `
            <div id="campaign-wise-lead-doc-table"
                style="
                    background: #ffffff;
                    border: 1px solid #d1d8dd;
                    padding: 15px;
                    border-radius: 6px;
                    margin-bottom: 16px;
                    font-size: 13px;
                ">

                <b>📘 Campaign Wise Lead Report – Column Description</b>
                <br><br>

                <table style="
                    width: 80%;
                    border-collapse: collapse;
                    font-size: 13px;
                ">
                    <thead>
                        <tr style="background:#f5f7fa;">
                            <th style="border:1px solid #d1d8dd; padding:8px; width:20%;">Column</th>
                            <th style="border:1px solid #d1d8dd; padding:8px;">Description</th>
                            <th style="border:1px solid #d1d8dd; padding:8px; width:35%;">Conditions / Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td style="border:1px solid #d1d8dd; padding:8px;"><b>Campaign</b></td>
                            <td style="border:1px solid #d1d8dd; padding:8px;">
                                Displays the Campaign Name
                            </td>
                            <td style="border:1px solid #d1d8dd; padding:8px;">
                                Empty values shown as <b>Not Set</b>
                            </td>
                        </tr>

                        <tr>
                            <td style="border:1px solid #d1d8dd; padding:8px;"><b>Today Created</b></td>
                            <td style="border:1px solid #d1d8dd; padding:8px;">
                                Number of leads created today
                            </td>
                            <td style="border:1px solid #d1d8dd; padding:8px;">
                                <code>DATE(creation) = CURDATE()</code>
                            </td>
                        </tr>

                        <tr>
                            <td style="border:1px solid #d1d8dd; padding:8px;"><b>Today Lead Nurture</b></td>
                            <td style="border:1px solid #d1d8dd; padding:8px;">
                                Leads created today with qualified status
                            </td>
                            <td style="border:1px solid #d1d8dd; padding:8px;">
                                Interested, Quotation, Opportunity, Converted
                            </td>
                        </tr>

                        <tr>
                            <td style="border:1px solid #d1d8dd; padding:8px;"><b>Total Leads</b></td>
                            <td style="border:1px solid #d1d8dd; padding:8px;">
                                Total number of leads per campaign
                            </td>
                            <td style="border:1px solid #d1d8dd; padding:8px;">
                                All leads
                            </td>
                        </tr>

                        <tr>
                            <td style="border:1px solid #d1d8dd; padding:8px;"><b>Contacted Today</b></td>
                            <td style="border:1px solid #d1d8dd; padding:8px;">
                                Leads updated today
                            </td>
                            <td style="border:1px solid #d1d8dd; padding:8px;">
                                Status change or any update<br>
                                Excludes Administrator<br>
                                <code>DATE(modified) = CURDATE()</code>
                            </td>
                        </tr>

                        <tr>
                            <td style="border:1px solid #d1d8dd; padding:8px;"><b>Pending Contact</b></td>
                            <td style="border:1px solid #d1d8dd; padding:8px;">
                                Leads pending follow-up
                            </td>
                            <td style="border:1px solid #d1d8dd; padding:8px;">
                                Open, Lead
                            </td>
                        </tr>

                        <tr>
                            <td style="border:1px solid #d1d8dd; padding:8px;"><b>Interested Count</b></td>
                            <td style="border:1px solid #d1d8dd; padding:8px;">
                                Leads showing interest
                            </td>
                            <td style="border:1px solid #d1d8dd; padding:8px;">
                                Interested, Lead, Quotation, Opportunity, Prospect
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        `;

        // ✅ Correct insertion (visible + safe)
        report.page.main.prepend(doc_table);
    },

    // ✅ Cleanup when user leaves this report
    onleave: function () {
        $("#campaign-wise-lead-doc-table").remove();
    }
};

