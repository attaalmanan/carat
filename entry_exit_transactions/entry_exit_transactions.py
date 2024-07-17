# Copyright (c) 2023, ARD and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import cint, today, flt
from frappe import _

class EntryExitTransactions(Document):
	def on_submit(self):
		self.make_journal_entry()
	# create journal entry from data in Doc
	def make_journal_entry(self):
		try:
			journal_entry = frappe.new_doc("Journal Entry")
			journal_entry.posting_date = today()
			journal_entry.user_remark = self.name
			journal_entry.custom_created_from = self.name or ""
			if(self.currency != frappe.defaults.get_user_default("currency")  ) :
				journal_entry.multi_currency = 1 
			if self.amount != 0 and self.debit and self.credit:
				journal_entry.append("accounts",
					{
					"account": self.debit,
					"credit_in_account_currency": 0 ,
					"debit_in_account_currency": flt(self.amount),
					}
				)
				journal_entry.append("accounts",
					{
					"account": self.credit, "party_type":"Customer",
					"party":self.customer,
					"credit_in_account_currency": flt(self.amount),
					"debit_in_account_currency": 0 
					}
				 )
				if (self.commission):
					if (self.transaction_type == "Entry") :
							journal_entry.append("accounts",
								{
								"account": self.credit, "party_type":"Customer",
								"party":self.customer,
								"credit_in_account_currency": 0,
								"debit_in_account_currency": flt(self.commission),
								}
							)
					elif (self.transaction_type == "Exit"):
							journal_entry.append("accounts",
								{
								"account": self.debit, "party_type":"Customer",
								"party":self.customer,
								"credit_in_account_currency": 0,
								"debit_in_account_currency": flt(self.commission),
								}
							)
					journal_entry.append("accounts",
						{
						"account": self.commission_account,
						"credit_in_account_currency": flt(self.commission),
						"debit_in_account_currency": 0 ,
						}
					)

				journal_entry.save()
				self.db_set("journal_entry", journal_entry.name)
				self.save()
				frappe.db.commit()

		except Exception as e:
			print(e)
			traceback = frappe.get_traceback()
			frappe.log_error(
			title=_("Error while creating journal entry for {}".format(self.name)),
			message=traceback,
			)
	  
@frappe.whitelist()
def fetch_fields_from_account_settings(transaction_type , branch , currency):
	debit = ""
	credit = ""
	commission = 0.0
	commission_account = ""
	accounts = frappe.get_single("Accounting Transactions Setting").entry_and_exit_transactions
	for account in accounts:
		if account.branch == branch and account.transaction_type == transaction_type and account.currency == currency :
			debit = account.debit
			credit = account.credit
			commission = account.commission
			commission_account  = account.commission_account
	return debit, credit , commission_account , commission
	  
@frappe.whitelist()
def fill_form_from_transaction_name(transaction_name ):
	debit = ""
	credit = ""
	commission = 0.0
	commission_account = ""
	branch = ""
	currency = ""
	transaction_type = ""
	accounts = frappe.get_single("Accounting Transactions Setting").entry_and_exit_transactions
	for account in accounts:
		if account.transaction_name == transaction_name :
			debit = account.debit
			credit = account.credit
			commission = account.commission
			commission_account  = account.commission_account
			branch = account.branch
			currency = account.currency
			transaction_type = account.transaction_type
	return debit, credit , commission_account , commission , branch , currency , transaction_type
