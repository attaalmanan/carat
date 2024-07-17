// Copyright (c) 2024, ARD and contributors
// For license information, please see license.txt
frappe.ui.form.on('Exchange Settings', {
	setup: function(frm) {
		const default_company = frappe.defaults.get_default('company');
	    frm.set_query('from_treasury','settings', function(doc, cdt, cdn) {
            let d = locals[cdt][cdn];
			var child = locals[cdt][cdn];
			var currencyValue = child.currency;
            return{
				filters: {
					account_type: ['in', ["Cash", "Bank", "Receivable"]],
					company: default_company,
					is_group: 0,
					account_currency: currencyValue
				}
			};
	    });

	    frm.set_query('trading_treasury','settings', function(doc, cdt, cdn) {
            let d = locals[cdt][cdn];
			var child = locals[cdt][cdn];
			var currencyValue = child.currency;
            return{
				filters: {
					account_type: ['in', ["Cash", "Bank", "Receivable"]],
					company: default_company,
					is_group: 0,
					account_currency: currencyValue
				}
			};
	    });


	}
});
