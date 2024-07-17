// Copyright (c) 2024, ARD and contributors
// For license information, please see license.txt

frappe.ui.form.on('Deposit', {
	setup:function(frm){
		
	},	
	refresh: function(frm) {
		if(frm.doc.workflow_state == 'Counted and Approved'){
			frm.disable_form()
		}

		var elements = document.querySelectorAll('div.col-sm-1');

		// Loop through each element and update its class
		elements.forEach(function(element) {
			element.classList.remove('col-sm-1');
			element.classList.add('col-sm-2');
		});
		var elements = document.querySelectorAll('input[data-fieldtype="Int"]');

		// Loop through each element and update its height
		elements.forEach(function(element) {
			element.style.setProperty('height', '70px', 'important');
			element.style.setProperty('font-size', 'x-large', 'important');
		});
		

		var elements = document.querySelectorAll('div[data-fieldtype="Int"]');
		elements.forEach(function(element) {
				// Get the label inside the same div as the input
				var label = element.querySelector("label");
				if (label) {
					label.style.setProperty('font-size', 'large', 'important');
			}
		});	
	
		
	
		

		let selectedField = null;
		const inputFields = document.querySelectorAll('input.input-with-feedback');
	
		inputFields.forEach((field) => {
			field.addEventListener('focus', function () {
				selectedField = this;
			});
		});
	
		const nums = document.querySelectorAll('.num');
		nums.forEach((button) => {
			button.addEventListener('click', function () {
				const num = parseInt(this.getAttribute('data-num'));
				appendToSelected(num);
				
			});
		});
		const deleteButton = document.querySelector('.delete');
		deleteButton.addEventListener('click', function () {
			if (selectedField) {
				selectedField.value = selectedField.value.slice(0, -1) || 0 ;
				frm.set_value(selectedField.getAttribute('data-fieldname'),parseInt(selectedField.value))

			}
		});

		const resetButton = document.querySelector('.reset');
		resetButton.addEventListener('click', function () {
			if (selectedField) {
				// selectedField.value = '';
				frm.set_value(selectedField.getAttribute('data-fieldname'),0)

			}
		});

		function appendToSelected(num) {

			if (selectedField) {
				selectedField.value += num;
				frm.set_value(selectedField.getAttribute('data-fieldname'),parseInt(selectedField.value))

			} else {
				alert('Please select a field first.');
			}
		}


		frm.set_query('debit', function(doc) {
			return {
				query: "carat.carat.doctype.deposit.deposit.query_fitler_for_account",
				filters: {
					currency: frm.doc.currency,
					customer_group: frm.doc.customer_group
				}
			};
		});
	},customer: function(frm){
		frm.save()
	},
	calc_money:function(frm){
		let total_rozma = 0;
		let total = 0;
		// let quarter_r = frm.doc.quarter_r *.25 *100;
		// let half_r = frm.doc.half_r *.5*100;
		// let one_r = frm.doc.one_r * 1*100;
		let five_r = frm.doc.five_r * 5*100;
		let ten_r = frm.doc.ten_r * 10*100;
		let twenty_r = frm.doc.twenty_r * 20*100;
		let fifty_r = frm.doc.fifty_r * 50*100;
		let hundred_r = frm.doc.hundred_r * 100*100;
		let twohundred_r = frm.doc.twohundred_r * 200*100;
		let fivehundred_r = frm.doc.fivehundred_r * 500*100;
		total_rozma = five_r + ten_r + twenty_r + fifty_r + hundred_r + twohundred_r + fivehundred_r 

		let quarter = frm.doc.quarter *.25
		let half = frm.doc.half *.5
		let one = frm.doc.one * 1;
		let five = frm.doc.five * 5;
		let ten = frm.doc.ten * 10;
		let twenty = frm.doc.twenty * 20;
		let fifty = frm.doc.fifty * 50;
		let hundred = frm.doc.hundred * 100;
		let twohundred = frm.doc.twohundred * 200;
		let fivehundred = frm.doc.fivehundred * 500;
		total = quarter + half + one + five + ten + twenty + fifty + hundred + twohundred + fivehundred + total_rozma
		frm.set_value("amount",total)
	},
	count_money:function(frm){
		let quarter = frm.doc.v_quarter *.25
		let half = frm.doc.v_half *.5
		let one = frm.doc.v_one * 1;
		let five = frm.doc.v_five * 5;
		let ten = frm.doc.v_ten * 10;
		let twenty = frm.doc.v_twenty * 20;
		let fifty = frm.doc.v_fifty * 50;
		let hundred = frm.doc.v_hundred * 100;
		let twohundred = frm.doc.v_twohundred * 200;
		let fivehundred = frm.doc.v_fivehundred * 500;
		let total_approved_amount = quarter + half + one + five + ten + twenty + fifty + hundred + twohundred + fivehundred 
		frm.set_value("total_approved_amount", total_approved_amount)
		// let total_damaged = frm.doc.amount - total_approved_amount
		// frm.set_value("total_damaged", total_damaged)

	},

	quarter: function(frm){
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
	},twohundred: function(frm){
		frm.trigger("calc_money")
	},fivehundred: function(frm){
		frm.trigger("calc_money")

	// },quarter_r: function(frm){
	// 	frm.trigger("calc_money")
	// },half_r: function(frm){
	// 	frm.trigger("calc_money")
	// },one_r: function(frm){
	// 	frm.trigger("calc_money")
	},five_r: function(frm){
		frm.trigger("calc_money")
	},ten_r: function(frm){
		frm.trigger("calc_money")
	},twenty_r: function(frm){
		frm.trigger("calc_money")
	},fifty_r: function(frm){
		frm.trigger("calc_money")
	},hundred_r: function(frm){
		frm.trigger("calc_money")
	},twohundred_r: function(frm){
		frm.trigger("calc_money")
	},fivehundred_r: function(frm){
		frm.trigger("calc_money")


	},v_quarter: function(frm){
		frm.trigger("count_money")
	},v_half: function(frm){
		frm.trigger("count_money")
	},v_one: function(frm){
		frm.trigger("count_money")
	},v_five: function(frm){
		frm.trigger("count_money")
	},v_ten: function(frm){
		frm.trigger("count_money")
	},v_twenty: function(frm){
		frm.trigger("count_money")
	},v_fifty: function(frm){
		frm.trigger("count_money")
	},v_hundred: function(frm){
		frm.trigger("count_money")
	},v_twohundred: function(frm){
		frm.trigger("count_money")
	},v_fivehundred: function(frm){
		frm.trigger("count_money")
	}
});


// 2*100*50
// entered number * 100 * type of field 

