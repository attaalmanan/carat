# Copyright (c) 2024, ARD and contributors
# For license information, please see license.txt

import frappe
import json
from frappe.model.document import Document
from datetime import date
from frappe import _, msgprint
from frappe.utils import cint, today, flt
from carat.api import make_journal_entry


class Transfer(Document):
	def validate(self):
		result = []
		settings_doc = frappe.get_single("Carat Settings")
		deposit_table =  settings_doc.transfer_settings
		for row in deposit_table:
			if row.currency == self.currency and row.customer_group == self.customer_group:
				result.append(str(row.debit))
		if len(result)==1:
			self.debit = result[0]
			self.multi = 0

		elif len(result)>1:
			self.multi = 1
			if not self.debit:
				self.debit = result[0]

		elif len(result)<1:
			frappe.throw("This transaction is not supported No info in Carat Settings about it, checkout with administrator")

			
		return result


	def on_submit(self):
		amount = 0
		rate = 0
		commission_amount = 0
		settings_doc = frappe.get_single("Carat Settings")
		deposit_table =  settings_doc.transfer_settings
		for row in deposit_table:
			if row.currency == self.currency and row.customer_group == self.customer_group and row.debit == self.debit:
				debit = row.debit
				credit = row.credit
				commission_account = row.commission_account
				commission_type = row.commission_type
				amount = row.amount
				rate = row.rate
				if commission_type == "Rate":
					commission_amount = flt(self.amount) * flt(rate) / 100
				if commission_type == "Amount":
					commission_amount = amount
				make_journal_entry(self, debit, credit, commission_account, commission_amount,transaction_type="transfer")
	  

@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def query_fitler_for_account(doctype, txt, searchfield, start, page_len, filters):
	return frappe.db.sql(
		"""select debit from `tabTransfer Settings table`
		where customer_group = %s and currency = %s
		and %s like %s order by name limit %s offset %s"""
		% ("%s","%s", searchfield, "%s", "%s", "%s"),
		(filters["customer_group"], filters["currency"], "%%%s%%" % txt, page_len, start),
		as_list=1,
	)
