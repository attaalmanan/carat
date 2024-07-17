# Copyright (c) 2024, ARD and contributors
# For license information, please see license.txt

import frappe
import json
from frappe.model.document import Document
from datetime import date
from frappe import _, msgprint
from frappe.utils import cint, today, flt
from carat.api import make_journal_entry, make_journal_entry_closing


class Withdraw(Document):
    def validate(self):
        # self.v_quarter = flt(self.quarter)
        # self.v_half = flt(self.half)
        # self.v_one = self.one
        # self.v_five = self.five
        # self.v_ten = self.ten
        # self.v_twenty = self.twenty
        # self.v_fifty = self.fifty
        # self.v_hundred = self.hundred
        # self.v_twohundred = self.twohundred
        # self.v_fivehundred = self.fivehundred

        quarter = flt(self.quarter) * 0.25
        half = flt(self.half) * 0.5
        one = self.one * 1
        five = self.five * 5
        ten = self.ten * 10
        twenty = self.twenty * 20
        fifty = self.fifty * 50
        hundred = self.hundred * 100
        twohundred = self.twohundred * 200
        fivehundred = self.custom_500 * 500
        custom_1000 = self.custom_1000 * 1000
        total = quarter + half + one + five + ten + twenty + fifty + hundred + twohundred + fivehundred + custom_1000
        self.amount = total
        # self.total_damaged = self.amount - self.total_approved_amount
        result = []
        settings_doc = frappe.get_single("Carat Settings")
        deposit_table = settings_doc.deposit
        for row in deposit_table:
            if row.currency == self.currency and row.customer_group == self.customer_group:
                result.append(str(row.debit))
        if len(result) == 1:
            self.debit = result[0]
            self.multi = 0
        elif len(result) > 1:
            self.multi = 1
            if not self.debit:
                self.debit = result[0]
        elif len(result) < 1:
            frappe.throw("This transaction is not supported No info in Carat Settings about it, checkout with administrator")
        return result

    def on_submit(self):
        if self.amount == 0:
            frappe.throw("Amount Should Not Equal Zero")
        amount = 0
        rate = 0
        commission_amount = 0
        settings_doc = frappe.get_single("Carat Settings")
        deposit_table = settings_doc.withdraw
        for row in deposit_table:
            if row.currency == self.currency and row.customer_group == self.customer_group:
                debit = row.debit
                credit = row.credit
                commission_account = row.commission_account
                commission_type = row.commission_type
                amount = row.amount
                rate = row.rate
                if commission_type == "Rate":
                    commission_amount = flt(self.amount) * flt(rate)
                if commission_type == "Amount":
                    commission_amount = amount
                make_journal_entry(self, debit, credit, commission_account, commission_amount,transaction_type="withdraw")

    # def before_update_after_submit(self):
    #     if self.workflow_state == 'Counted and Approved':
    #         settings_doc = frappe.get_single("Carat Settings")
    #         deposit_table = settings_doc.deposit
    #         for row in deposit_table:
    #             if row.currency == self.currency and row.customer_group == self.customer_group and row.debit == self.debit:
    #                 debit = row.debit
    #                 credit = row.credit
    #                 main_treasury = row.main_treasury
    #                 damaged_cash_treasury = row.damaged_cash_treasury
    #                 holding_treasury = row.holding_treasury
    #                 make_journal_entry_closing(self, debit, credit, main_treasury,
    #                                             damaged_cash_treasury, holding_treasury,
    #                                               transaction_type="withdraw")
@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def query_fitler_for_account(doctype, txt, searchfield, start, page_len, filters):
    return frappe.db.sql(
        """select debit from `tabWithdraw Settings table`
        where customer_group = %s and currency = %s
        and %s like %s order by name limit %s offset %s"""
        % ("%s","%s", searchfield, "%s", "%s", "%s"),
        (filters["customer_group"], filters["currency"], "%%%s%%" % txt, page_len, start),
        as_list=1,
    )

