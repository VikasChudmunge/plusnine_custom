(() => {
    // Compatibility for India Compliance source/assets version mismatch.
    // Its Purchase Invoice handler calls this during setup, but older cached
    // bundles do not expose the helper and abort the complete form render.
    if (typeof india_compliance !== "undefined" &&
        typeof india_compliance.setup_itc_claim_period_query !== "function") {
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

    if (typeof india_compliance !== "undefined" &&
        typeof india_compliance.set_itc_claim_period_status !== "function") {
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

    const Controller = typeof erpnext !== "undefined" && erpnext.accounts?.PurchaseInvoice;
    if (!Controller) {
        return;
    }

    const parent_setup = Object.getPrototypeOf(Controller.prototype)?.setup;

    Controller.prototype.setup = function(doc) {
        if (typeof parent_setup === "function") {
            parent_setup.call(this, doc);
        }

        if (typeof this.setup_accounting_dimension_triggers === "function") {
            this.setup_accounting_dimension_triggers();
        }

        if (typeof this.setup_posting_date_time_check === "function") {
            this.setup_posting_date_time_check();
        }
    };

    if (typeof cur_frm !== "undefined" && cur_frm?.cscript) {
        cur_frm.cscript.setup = Controller.prototype.setup;
    }
})();
