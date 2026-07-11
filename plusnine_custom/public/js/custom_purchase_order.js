(() => {
    const Controller = typeof erpnext !== "undefined" && erpnext.buying?.PurchaseOrderController;
    if (!Controller) {
        return;
    }

    const parent_setup = Object.getPrototypeOf(Controller.prototype)?.setup;

    Controller.prototype.setup = function() {
        if (typeof parent_setup === "function") {
            parent_setup.call(this);
        }

        if (typeof this.setup_accounting_dimension_triggers === "function") {
            this.setup_accounting_dimension_triggers();
        }

        this.frm.custom_make_buttons = {
            "Purchase Receipt": "Purchase Receipt",
            "Purchase Invoice": "Purchase Invoice",
            "Payment Entry": "Payment",
            "Subcontracting Order": "Subcontracting Order",
            "Stock Entry": "Material to Supplier",
        };
    };

    if (typeof cur_frm !== "undefined" && cur_frm?.cscript) {
        cur_frm.cscript.setup = Controller.prototype.setup;
    }
})();
