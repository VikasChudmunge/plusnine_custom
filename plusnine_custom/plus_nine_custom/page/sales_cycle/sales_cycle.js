frappe.pages["sales-cycle"].on_page_load = function (wrapper) {
	frappe.ui.make_app_page({
		parent: wrapper,
		title: __("Sales Cycle"),
		single_column: true,
	});

	const $body = $(wrapper).find(".layout-main-section");
	$body.empty();

	ensure_sales_cycle_styles();

	const stages = [
		{ key: "sales_order", label: "Sales Order" },
		{ key: "delivery_note", label: "Delivery Note" },
		{ key: "sales_invoice", label: "Sales Invoice" },
		{ key: "payment_entry", label: "Payment Entry" },
	];

	const $header = $(
		`<div class="pn-cycle-header">
			<div>
				<h3 class="pn-cycle-title">${__("Sales Cycle")}</h3>
				<p class="text-muted">${__(
					"Use the tabs to start from any stage and expand to the next steps."
				)}</p>
			</div>
		</div>`
	);
	$body.append($header);

	const $tabs = $('<ul class="nav nav-tabs pn-cycle-tabs" role="tablist"></ul>');
	const $content = $('<div class="tab-content pn-cycle-tab-content"></div>');
	$body.append($tabs, $content);

	stages.forEach((stage, index) => {
		const isActive = index === 0;
		const $tabItem = $('<li class="nav-item"></li>');
		const $tabLink = $(
			`<a class="nav-link${isActive ? " active" : ""}" href="#" data-stage="${
				stage.key
			}">${__(stage.label)}</a>`
		);
		$tabItem.append($tabLink);
		$tabs.append($tabItem);

		const $pane = $(
			`<div class="tab-pane${isActive ? " active" : ""}" data-stage="${stage.key}"></div>`
		);
		const $treeWrap = $('<div class="pn-cycle-tree-wrap"></div>');
		$pane.append($treeWrap);
		$content.append($pane);

		$tabLink.on("click", (event) => {
			event.preventDefault();
			$tabs.find(".nav-link").removeClass("active");
			$tabLink.addClass("active");
			$content.find(".tab-pane").removeClass("active");
			$pane.addClass("active");
			ensure_tree_loaded(stage.key, $treeWrap);
		});

		if (isActive) {
			ensure_tree_loaded(stage.key, $treeWrap);
		}
	});
};

function ensure_tree_loaded(stage, $treeWrap) {
	if ($treeWrap.data("tree-loaded")) {
		return;
	}

	new frappe.ui.Tree({
		parent: $treeWrap,
		label: __(get_stage_label(stage)),
		expandable: true,
		method: "plusnine_custom.plus_nine_custom.page.cycle_tree.get_cycle_tree",
		args: { cycle: "sales", stage },
		get_label(node) {
			return __(node.data.display_label || node.label);
		},
		on_click(node) {
			if (node.data && node.data.route && !node.expandable) {
				frappe.set_route(...node.data.route);
			}
		},
	});

	$treeWrap.data("tree-loaded", true);
}

function get_stage_label(stage) {
	const labels = {
		sales_order: __("Sales Orders"),
		delivery_note: __("Delivery Notes"),
		sales_invoice: __("Sales Invoices"),
		payment_entry: __("Payment Entries"),
	};
	return labels[stage] || __("Sales Cycle");
}

function ensure_sales_cycle_styles() {
	if (document.getElementById("pn-sales-cycle-style")) {
		return;
	}

	frappe.dom.set_style(
		`
		.pn-cycle-header {
			display: flex;
			align-items: center;
			justify-content: space-between;
			margin-bottom: 16px;
			padding: 16px 18px;
			border-radius: 16px;
			background: linear-gradient(120deg, #fff7e6 0%, #ffffff 55%, #fff1d6 100%);
			border: 1px solid #f1dfbf;
			box-shadow: 0 12px 28px rgba(0, 0, 0, 0.06);
		}
		.pn-cycle-title {
			margin-bottom: 4px;
			letter-spacing: 0.2px;
		}
		.pn-cycle-tabs {
			border-bottom: none;
			gap: 8px;
			flex-wrap: wrap;
		}
		.pn-cycle-tabs .nav-link {
			border: 1px solid var(--gray-200);
			border-radius: 999px;
			padding: 6px 14px;
			color: var(--text-color);
			font-weight: 600;
			background: #ffffff;
			box-shadow: 0 6px 14px rgba(0, 0, 0, 0.05);
			transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
		}
		.pn-cycle-tabs .nav-link.active {
			color: #7a5b1a;
			border-color: #e7c98d;
			background: linear-gradient(120deg, #fff4df, #fffdf7);
			box-shadow: 0 10px 20px rgba(0, 0, 0, 0.08);
			transform: translateY(-1px);
		}
		.pn-cycle-tabs .nav-link:hover {
			box-shadow: 0 10px 20px rgba(0, 0, 0, 0.08);
			transform: translateY(-1px);
		}
		.pn-cycle-tab-content {
			margin-top: 16px;
		}
		.pn-cycle-tree-wrap {
			background: radial-gradient(circle at top left, #fff7e6, #ffffff 50%);
			border: 1px solid #f1dfbf;
			border-radius: 18px;
			padding: 18px;
			box-shadow: 0 12px 28px rgba(0, 0, 0, 0.06);
		}
		.pn-cycle-tree-wrap .tree {
			background: transparent;
		}
		.pn-cycle-tree-wrap .tree-link {
			display: inline-flex;
			align-items: center;
			gap: 8px;
			padding: 6px 10px;
			border-radius: 10px;
			transition: background 0.2s ease, transform 0.2s ease;
		}
		.pn-cycle-tree-wrap .tree-link.selected {
			background: #fff1d6;
			box-shadow: inset 0 0 0 1px #f0d29a;
		}
		.pn-cycle-tree-wrap .tree-link:hover {
			background: #fff4e2;
			transform: translateX(2px);
		}
		.pn-cycle-tree-wrap .tree-label {
			font-weight: 600;
			color: var(--text-color);
		}
		.pn-cycle-tree-wrap .tree-children {
			margin-top: 6px;
			border-left: 1px dashed #e4d3b3;
		}
		@media (max-width: 768px) {
			.pn-cycle-tree-wrap {
				padding: 12px;
			}
			.pn-cycle-header {
				padding: 12px 14px;
			}
		}
	`,
		"pn-sales-cycle-style"
	);
}
