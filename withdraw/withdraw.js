// Copyright (c) 2024, ARD and contributors
// For license information, please see license.txt

frappe.ui.form.on('Withdraw', {
	setup:function(frm){
		// numpad.init();
		// numpad.attach({ target: document.querySelectorAll('[data-fieldname="quarter"]')[0] });
		// numpad.attach({ target: document.querySelectorAll('[data-fieldname="half"]')[0] });
		// numpad.attach({ target: document.querySelectorAll('[data-fieldname="one"]')[0] });
		// numpad.attach({ target: document.querySelectorAll('[data-fieldname="five"]')[0] });
		// numpad.attach({ target: document.querySelectorAll('[data-fieldname="ten"]')[0] });
		// numpad.attach({ target: document.querySelectorAll('[data-fieldname="twenty"]')[0] });
		// numpad.attach({ target: document.querySelectorAll('[data-fieldname="fifty"]')[0] });
		// numpad.attach({ target: document.querySelectorAll('[data-fieldname="hundred"]')[0] });
		// numpad.attach({ target: document.querySelectorAll('[data-fieldname="thouthnd"]')[0] });
		// numpad.attach({ target: document.querySelectorAll('[data-fieldname="fivehundred"]')[0] });
	},
	refresh: function(frm) {
		frm.set_query('debit', function(doc) {
			return {
				query: "carat.carat.doctype.withdraw.withdraw.query_fitler_for_account",
				filters: {
					currency: frm.doc.currency,
					customer_group: frm.doc.customer_group,
					
				}
			};
		});
	}
	,customer: function(frm){
		frm.save()
	},
	calc_money:function(frm){
		let quarter = frm.doc.quarter *.25
		let half = frm.doc.half *.5
		let one = frm.doc.one * 1;
		let five = frm.doc.five * 5;
		let ten = frm.doc.ten * 10;
		let twenty = frm.doc.twenty * 20;
		let fifty = frm.doc.fifty * 50;
		let hundred = frm.doc.hundred * 100;
		let thouthnd = frm.doc.custom_1000 * 1000;
		let fivehundred = frm.doc.custom_500 * 500;  
		let tht = frm.doc.custom_2000 * 2000; 
		let tht5 = frm.doc.custom_5000 * 5000;
		
		let total = quarter + half + one + five + ten + twenty + fifty + hundred + thouthnd + fivehundred +tht +tht5
		frm.set_value("amount",total)
	//	frm.refresh(total)
	//},
	//    count_money:function(frm){
	// 	 let quarter = frm.doc.v_quarter *.25
	// 	 let half = frm.doc.v_half *.5
	// 	 let one = frm.doc.v_one * 1;
	// 	 let five = frm.doc.v_five * 5;
	// 	 let ten = frm.doc.v_ten * 10;
	// 	 let twenty = frm.doc.v_twenty * 20;
	// 	 let fifty = frm.doc.v_fifty * 50;
	// 	 let hundred = frm.doc.v_hundred * 100;
	// 	 let thouthnd = frm.doc.v_thouthnd * 1000;
	// 	 let fivehundred = frm.doc.v_fivehundred * 500;
	// 	 let total_approved_amount = quarter + half + one + five + ten + twenty + fifty + hundred + thouthnd + fivehundred 
	// 	 frm.set_value("amount", total_approved_amount)
		 // let total_damaged = frm.doc.amount - total_approved_amount
		 // frm.set_value("total_damaged", total_damaged)

	},quarter: function(frm){
		frm.trigger("calc_money")
	},half: function(frm){
		frm.trigger("calc_money")
	},one: function(frm){
		frm.trigger("calc_money")
	},five: function(frm){
		frm.trigger("calc_money")
	},ten: function(frm){
		frm.trigger("calc_money")
	},twenty: function(frm){
		frm.trigger("calc_money")
	},fifty: function(frm){
		frm.trigger("calc_money")
	},hundred: function(frm){
		frm.trigger("calc_money")
	},custom_500: function(frm){
		frm.trigger("calc_money")
	},custom_1000: function(frm){
		frm.trigger("calc_money")
	},custom_2000: function(frm){
		frm.trigger("calc_money")
	},custom_5000: function(frm){
		frm.trigger("calc_money")







	},
	// v_quarter: function(frm){
	// 	frm.trigger("count_money")
	// },v_half: function(frm){
	// 	frm.trigger("count_money")
	// },v_one: function(frm){
	// 	frm.trigger("count_money")
	// },v_five: function(frm){
	// 	frm.trigger("count_money")
	// },v_ten: function(frm){
	// 	frm.trigger("count_money")
	// },v_twenty: function(frm){
	// 	frm.trigger("count_money")
	// },v_fifty: function(frm){
	// 	frm.trigger("count_money")
	// },v_hundred: function(frm){
	// 	frm.trigger("count_money")
	// },v_thouthnd: function(frm){
	// 	frm.trigger("count_money")
	// },v_fivehundred: function(frm){
	// 	frm.trigger("count_money")
	// }
});