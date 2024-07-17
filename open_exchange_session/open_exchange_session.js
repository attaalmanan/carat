// Copyright (c) 2024, ARD and contributors
// For license information, please see license.txt

frappe.ui.form.on('Open Exchange Session', {
	refresh: function(frm){
		if (frm.doc.docstatus==1 && frm.doc.closed ==0 ) {
				frm.add_custom_button(__("Close Exchange Session"), function() {
					frm.trigger("close_exchange_session");
				})
			}
	}, 
	after_save: function(frm) {
		location.reload();
    },
	close_exchange_session:function(frm){

		frappe.call({
			method: "close_exchange_journal_entry",
			doc: frm.doc,
			callback: function(r) {
				if (r.message) {
					location.reload();
				}
			}
		})

	},
	setup: function(frm) {
		frm.set_query('currency','exchange_table', function(doc, cdt, cdn) {
			var child = locals[cdt][cdn];
			return{
				query: "carat.carat.doctype.open_exchange_session.open_exchange_session.query_fitler_for_account",
				filters: {
					is_group: 0,
					employee: frm.doc.employee
				}

			};
		});
		frm.set_query('from_treasury','exchange_table', function(doc, cdt, cdn) {
			var child = locals[cdt][cdn];
			var currencyValue = child.currency;
			return{
				query: "carat.carat.doctype.open_exchange_session.open_exchange_session.query_fitler_for_account_from_treasury",
				filters: {
					currency: currencyValue,
					employee: frm.doc.employee

				}
			};
		});
		frm.set_query('trading_treasury','exchange_table', function(doc, cdt, cdn) {
			var child = locals[cdt][cdn];
			var currencyValue = child.currency;
			return{
				query: "carat.carat.doctype.open_exchange_session.open_exchange_session.query_fitler_for_account_trading_treasury",
				filters: {
					currency: currencyValue,
					employee: frm.doc.employee

				}
			};
		});
		frm.set_query('profit_loss_treasury','exchange_table', function(doc, cdt, cdn) {
			var child = locals[cdt][cdn];
			var currencyValue = child.currency;
			return{
				query: "carat.carat.doctype.open_exchange_session.open_exchange_session.query_fitler_for_account_profit_loss_treasury",
				filters: {
					currency: currencyValue,
					employee: frm.doc.employee

				}
			};
		});
		
		frm.set_query('from_currency','daily_trading', function(doc, cdt, cdn) {
			var child = locals[cdt][cdn];
			return {
				query: "carat.carat.doctype.open_exchange_session.open_exchange_session.query_fitler_for_account_exchange",
				filters: {
					open_exchange_session: frm.doc.name,
				}
			};
		});
		frm.set_query('to_currency','daily_trading', function(doc, cdt, cdn) {
			var child = locals[cdt][cdn];
			return {
				query: "carat.carat.doctype.open_exchange_session.open_exchange_session.query_fitler_for_account_exchange",
				filters: {
					open_exchange_session: frm.doc.name,
				}
			};
		});
	},calculate_total:function(frm, row){
		if (row.exchange_rate>=0 && row.from_amount >=1 ){
			row.exchange_rate = row.to_amount/row.from_amount
			row.to_amount = row.exchange_rate*row.from_amount
			frm.refresh_fields()
		}
	}

});

frappe.ui.form.on('Exchange Table For Opening', {	
	exchange_rate:function(frm, cdt, cdn) {
		var row = locals[cdt][cdn];

		if (row.exchange_rate>=0 && row.from_amount >=1 ){
			let exchange_rate = row.exchange_rate
			let from_amount = row.from_amount
			row.to_amount = exchange_rate*from_amount
			frm.refresh_fields()
		}
	},
	to_amount:function(frm, cdt, cdn) {
		var row = locals[cdt][cdn];
		if (row.exchange_rate>=0 && row.from_amount >=1 ){
			let from_amount = row.from_amount
			let to_amount = row.to_amount
			row.exchange_rate = to_amount/from_amount
			frm.refresh_fields()
		}
	},
	from_amount:function(frm,cdt,cdn){
		var row = locals[cdt][cdn];
		frm.events.calculate_total(frm, row);
	},
	from_amount:function(frm,cdt,cdn){
		var row = locals[cdt][cdn];
		frm.events.calculate_total(frm, row);
	},
});

///dailog

frappe.ui.form.on(' Open Exchange Session', {
	refresh: function(frm){
if (frm.is_new()){
	frm.add_custom_button("Set Status", () => {
		let d = new frappe.ui.Dialog({
			title: 'Set Status of the Property',
			fields: [
				{
					label: 'Status',
					fieldname: 'status',
					fieldtype: 'Select',
					options: [
						"Open",
						"Closed"
					],
					reqd: 1
				},
			],
			size: 'small', // small, large, extra-large 
			primary_action_label: 'Submit',
			primary_action(values) {
				/////////////
				//How to add a new row in a child table
				// var d = frm.add_child("features");
				// d.feature = values.feature
				// d.number_of_feature = values.number_of_feature

				// frm.refresh_field("feautres")

				////////////
				frm.set_value("status", values.status)
				d.hide();
			}
		});
		
		d.show();
	})
}
	}
})
	