(() => {
    // Keep Bill of Entry usable when India Compliance's Python/doctype code is
    // newer than its compiled desk bundle. The doctype calls these helpers
    // during setup and refresh, so a missing helper prevents a new form from
    // rendering at all.
    if (typeof india_compliance === "undefined") {
        return;
    }

    if (typeof india_compliance.setup_itc_claim_period_query !== "function") {
        india_compliance.setup_itc_claim_period_query = function(frm) {
            if (!frm.fields_dict.itc_claim_period) {
                return;
            }

            frm.set_query("itc_claim_period", () => ({
                query: "india_compliance.gst_india.utils.itc_claim.get_itc_period_options",
                params: {
                    company_gstin: frm.doc.company_gstin,
                    posting_date: frm.doc.posting_date,
                },
            }));
        };
    }

    if (typeof india_compliance.set_itc_claim_period_status !== "function") {
        india_compliance.set_itc_claim_period_status = function(frm) {
            if (!frm.fields_dict.itc_claim_period) {
                return;
            }

            frm.set_df_property("itc_claim_period", "ignore_validation", 1);

            const is_filed = frm.doc.__onload?.is_itc_period_filed;
            frm.set_df_property("itc_claim_period", "read_only", is_filed ? 1 : 0);
            frm.set_df_property(
                "itc_claim_period",
                "description",
                is_filed
                    ? __("GSTR-3B for {0} is filed", [frm.doc.itc_claim_period])
                    : __("GSTR-3B period for claiming ITC (MMYYYY) or 'Deferred' to postpone."),
            );
        };
    }

    if (typeof india_compliance.set_reconciliation_status !== "function") {
        india_compliance.set_reconciliation_status = function(frm, fieldname) {
            if (frm.doc.docstatus !== 1 || !frm.doc.reconciliation_status) {
                return;
            }

            const field = frm.get_field(fieldname);
            if (!field) {
                return;
            }

            const colors = {
                Reconciled: "green",
                Unreconciled: "red",
                Ignored: "grey",
                "Not Applicable": "grey",
                "Match Found": "yellow",
            };
            const color = colors[frm.doc.reconciliation_status] || "grey";

            field.set_description(
                `<div class="d-flex indicator ${color}">` +
                    `2A/2B Status:&nbsp;<strong>${frm.doc.reconciliation_status}</strong>` +
                "</div>",
            );
        };
    }
})();
