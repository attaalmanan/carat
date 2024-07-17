
// frappe.ui.form.on('Carat Settings', {
// 	setup: function(frm) {
// 	    frm.set_query('debit','deposit', function(doc, cdt, cdn) {
//             let d = locals[cdt][cdn];
// 			var child = locals[cdt][cdn];
// 			var currencyValue = child.currency;
// 			const default_company = frappe.defaults.get_default('company');

//             return{
// 				filters: {
// 					account_type: ['in', ["Cash", "Bank", "Receivable"]],
// 					company: default_company,
// 					is_group: 0,
// 					account_currency: currencyValue
// 				}
// 			};
// 	    });
// 	}
// });



frappe.ui.form.on('Carat Settings', {
	setup: function(frm) {
		const default_company = frappe.defaults.get_default('company');
	    frm.set_query('debit','deposit', function(doc, cdt, cdn) {
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

	    frm.set_query('credit','deposit', function(doc, cdt, cdn) {
            let d = locals[cdt][cdn];
			var child = locals[cdt][cdn];
			var currencyValue = child.currency;
            return{
				filters: {
					account_type: "Receivable",
					company: default_company,
					is_group: 0,
					account_currency: currencyValue
				}
			};
	    });

	    frm.set_query('main_treasury','deposit', function(doc, cdt, cdn) {
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
		frm.set_query('damaged_cash_treasury','deposit', function(doc, cdt, cdn) {
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
		frm.set_query('holding_treasury','deposit', function(doc, cdt, cdn) {
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

		
		frm.set_query('debit','withdraw', function(doc, cdt, cdn) {
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

	    frm.set_query('credit','withdraw', function(doc, cdt, cdn) {
            let d = locals[cdt][cdn];
			var child = locals[cdt][cdn];
			var currencyValue = child.currency;
            return{
				filters: {
					account_type: ['in', ["Cash", "Payable"]],
					company: default_company,
					is_group: 0,
					account_currency: currencyValue
				}
			};
	    });

	    frm.set_query('main_treasury','withdraw', function(doc, cdt, cdn) {
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
		frm.set_query('damaged_cash_treasury','withdraw', function(doc, cdt, cdn) {
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
		frm.set_query('holding_treasury','withdraw', function(doc, cdt, cdn) {
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



		frm.set_query('debit','transfer_settings', function(doc, cdt, cdn) {
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

	    frm.set_query('credit','transfer_settings', function(doc, cdt, cdn) {
            let d = locals[cdt][cdn];
			var child = locals[cdt][cdn];
			var currencyValue = child.currency;
            return{
				filters: {
					account_type: "Payable",
					company: default_company,
					is_group: 0,
					account_currency: currencyValue
				}
			};
	    });
	},
});

