(() => {
    const Controller = typeof erpnext !== "undefined" && erpnext.stock?.PurchaseReceiptController;
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

        this.frm.set_query("expense_account", "items", () => ({
            query: "erpnext.controllers.queries.get_expense_account",
            filters: {
                company: this.frm.doc.company,
                disabled: 0,
            },
        }));
    };

    if (typeof cur_frm !== "undefined" && cur_frm?.cscript) {
        cur_frm.cscript.setup = Controller.prototype.setup;
    }
})();
