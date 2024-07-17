// Copyright (c) 2023, ARD and contributors
// For license information, please see license.txt

frappe.ui.form.on('Entry Exit Transactions', {
	// refresh: function(frm) {

	// }
});

frappe.ui.form.on('Entry Exit Transactions', {
	onload: function(frm) {
		frm.set_query("customer", function(doc) {
			return {
				filters: {
					"default_currency": frm.doc.currency,
				}
			};
		});
	frm.set_query("transaction_name", function(doc) {
		return {
			filters: {
				"branch": frm.doc.branch,
			}
		};
	});
	},
	

	amount: function(frm) {
		frm.set_value('commission' , (frm.doc.commission_rate * frm.doc.amount / 100))
	
	},
	

	transaction_name : function(frm) {  
			fill_form_from_transaction_name(frm)
	}
});

// var full_form_fromaccount_setting =function(frm) {
// 	frappe.call({
// 		method: "carat.carat.doctype.entry_exit_transactions.entry_exit_transactions.fetch_fields_from_account_settings",
// 		args: {
// 			branch  : frm.doc.branch,
// 			transaction_type  : frm.doc.transaction_type,
// 			currency : frm.doc.currency
// 		},
// 		callback: (response) => {
// 			// console.log(response.message[0]);
// 			frm.set_value('debit' , response.message[0])
// 			frm.set_value('credit' , response.message[1])
// 			frm.set_value('commission_account' , response.message[2])
// 			frm.set_value('commission_rate' , response.message[3])
// 		}
// 	});
// }
var fill_form_from_transaction_name =function(frm) {
	frappe.call({
		method: "carat.carat.doctype.entry_exit_transactions.entry_exit_transactions.fill_form_from_transaction_name",
		args: {
			transaction_name  : frm.doc.transaction_name,
		},
		callback: (response) => {
			// console.log(response.message[0]);
			frm.set_value('debit' , response.message[0])
			frm.set_value('credit' , response.message[1])
			frm.set_value('commission_account' , response.message[2])
			frm.set_value('commission_rate' , response.message[3])
			frm.set_value('branch' , response.message[4])
			frm.set_value('currency' , response.message[5])
			frm.set_value('transaction_type' , response.message[6])
		}
	});
}