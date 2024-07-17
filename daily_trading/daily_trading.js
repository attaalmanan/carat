// Copyright (c) 2024, ARD and contributors
// For license information, please see license.txt

frappe.ui.form.on('Daily Trading', {
	refresh: function(frm) {
		$(".layout-side-section").hide()

		frappe.call({
			method: "carat.api.get_active_session",
			// args: {
			// 	role_profile: frm.doc.role_profile_name,
			// },
			callback: function (data) {
				let currencies = data.message.allowed_currency
				let employee = data.message.employee
				let currency_symbol = data.message.currency_symbol

				let from_currency = '<div>\n<label for="fromCurrency">From:</label><br>\n';
				let to_currency = '<div>\n<label for="toCurrency">To:</label><br>\n';

				for (let currency of currencies) {
					from_currency += `<input type="radio" id="${currency.toLowerCase()}" name="fromCurrency" value="${currency}"${currency === 'USD' ? ' checked' : ''}>\n`;
					from_currency += `<label for="${currency.toLowerCase()}">${currency}</label><br>\n`;
					to_currency += `<input type="radio" id="${currency.toLowerCase()}" name="toCurrency" value="${currency}"${currency === 'USD' ? ' checked' : ''}>\n`;
					to_currency += `<label for="${currency.toLowerCase()}">${currency}</label><br>\n`;
				}

				from_currency += '</div>';
				to_currency += '</div>';


				

				let html = `
				<div id="fad">
				<h1>مرحبا :  ${employee} </h1>
				<h1>Daily Trading </h1>
				<form id="currencyForm">
					${from_currency}
					<div class>
						<label for="fromAmount">Amount:</label><br>
						<input type="text" id="fromAmount" name="fromAmount" required="">
					</div>
					<div>
						<label for="exchangeRate">Exchange Rate:</label><br>
						<input type="text" id="exchangeRate" name="exchangeRate" required="">
					</div>
					<div>
						<button type="button" onclick="cur_frm.trigger('calculate')">Calculate</button>
					</div>

					<div>

					${to_currency}
					
					<div></div><!-- Empty div for spacing -->
					<div></div><!-- Empty div for spacing -->
					<div>
						<label for="toAmount">Result:</label><br>
						<input type="text" id="toAmount" name="toAmount" readonly="">
					</div>
					</div>

				</form>
				</div>


				`

				const fromCurrency =  `<div class="container">
				<div class="radio-tile-group">
			  
				 ${Object.keys(currency_symbol).map((row)=> `<div class="input-container">
					<input id="${row}" class="radio-button" type="radio" name="radio" />
					<div class="radio-tile">
					  <div class="icon walk-icon">
					  <p>${currency_symbol[row]}</p>
					  </div>
					  <label for="walk" class="radio-tile-label">${row}</label>
					</div>
				  </div>`
			  )}
				 
				</div>
			  </div>`
				
			

			  const toCurrency =  `<div class="container">
			  <div class="radio-tile-group">
			
			   ${Object.keys(currency_symbol).map((row)=> `<div class="input-container">
				  <input id="${row}" class="radio-button" type="radio" name="radio-to" />
				  <div class="radio-tile">
					<div class="icon walk-icon">
					<p>${currency_symbol[row]}</p>
					</div>
					<label for="walk" class="radio-tile-label">${row}</label>
				  </div>
				</div>`
			)}
			   
			  </div>
			</div>`


				let x = `<!DOCTYPE html>
				<html lang="en">
				  <head>
					<meta charset="UTF-8" />
					<meta name="viewport" content="width=device-width, initial-scale=1.0" />
					<link rel="stylesheet" href="css/style.css" />
					<link
					  rel="stylesheet"
					  href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.2.1/css/all.min.css"
					/>
				  </head>
				  <body>
					<div class="cu-container">
					  <div class="wrapper">
						<form>
						  <div class="amount">
							<p>Amount</p>
							<input type="text" value="1" />
						  </div>

						  <div class="amount">
							<p>Exchange Rate:</p>
							<input type="text" value="" />
						  </div>
						  <div class="convert_box">
							<div class="from">
							  <p>From</p>
							  ${fromCurrency}
							</div>
							<div class="reverse"><i class="fas fa-exchange-alt"></i></div>
							<div class="to">
							  <p>To</p>
							${toCurrency}
							</div>
						  </div>
						</form>
					  </div>
					  <button type="button">Exchange</button>
					</div>
				  </body>
				</html>
				`

				console.log(fromCurrency ,"fromCurrency")
				const role_area = $(x).appendTo(
					frm.fields_dict.html.wrapper
				);
		
		
			},
		});
	},calculate:function(frm) {
		console.log("SSS")
        const fromCurrency = document.querySelector('input[name="fromCurrency"]:checked').value;
        const toCurrency = document.querySelector('input[name="toCurrency"]:checked').value;
        const fromAmount = parseFloat(document.getElementById('fromAmount').value);
        const exchangeRate = parseFloat(document.getElementById('exchangeRate').value);
        let result;

        if (fromCurrency === 'USD') {
            result = fromAmount * exchangeRate;
        } else {
            result = fromAmount / exchangeRate;
        }

        document.getElementById('toAmount').value = result.toFixed(2) + ' ' + toCurrency;
    }

});



