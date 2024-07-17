// Copyright (c) 2024, ARD and contributors
// For license information, please see license.txt

frappe.ui.form.on('Transfer', {
	refresh: function(frm) {
		frm.set_query('debit', function(doc) {
			return {
				query: "carat.carat.doctype.transfer.transfer.query_fitler_for_account",
				filters: {
					currency: frm.doc.currency,
					customer_group: frm.doc.customer_group
				}
			};
		});
	}
});
