# Copyright (c) 2024, ARD and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from carat.api import open_exchange_journal_entry, close_exchange_journal_entry
from frappe.utils import cint, today, flt


class OpenExchangeSession(Document):

    # create journal entry from data in Doc
    def close_exchange_journal_entry(self, exchange_table, type_of_je):
        frappe.msgprint("welcome")
        try:
            journal_entry = frappe.new_doc("Journal Entry")
            journal_entry.posting_date = today()
            journal_entry.user_remark = self.name
            journal_entry.multi_currency = 1
            for row in exchange_table:
                # amount what we take  , total is the end total after trading
                if row.total > row.amount:
                    # if we return money more than we take, profit
                    journal_entry.append("accounts",
                                        {
                                            "account": row.from_treasury,
                                            "credit_in_account_currency": row.amount,
                                            "debit_in_account_currency": 0,
                                            "exchange_rate":   row.last_exchange_rate
                                        }
                                        )

                    journal_entry.append("accounts",
                                        {
                                            "account": row.trading_treasury,
                                            "credit_in_account_currency": row.total,
                                            "debit_in_account_currency": 0,
                                            "exchange_rate": row.last_exchange_rate
                                        }
                                        )
                    journal_entry.append("accounts",
                                        {
                                            "account": row.trading_treasury,
                                            "credit_in_account_currency": 0,
                                            "debit_in_account_currency": flt(row.total) - flt(row.amount),
                                            "exchange_rate": row.profit_loss_treasury
                                        }
                                        )
                # amount what we take  , total is the end total after trading
                if row.total < row.amount:
                    # if we return money less than we take, loss
                    journal_entry.append("accounts",
                                        {
                                            "account": row.from_treasury,
                                            "credit_in_account_currency": row.amount,
                                            "debit_in_account_currency": 0,
                                            "exchange_rate":   row.last_exchange_rate
                                        }
                                        )

                    journal_entry.append("accounts",
                                        {
                                            "account": row.trading_treasury,
                                            "credit_in_account_currency": row.total,
                                            "debit_in_account_currency": 0,
                                            "exchange_rate": row.last_exchange_rate
                                        }
                                        )
                    journal_entry.append("accounts",
                                        {
                                            "account": row.trading_treasury,
                                            "credit_in_account_currency": 0,
                                            "debit_in_account_currency": flt(row.total) - flt(row.amount),
                                            "exchange_rate": row.profit_loss_treasury
                                        }
                                        )
                # amount what we take  , total is the end total after trading
                if row.total == row.amount:
                    # if we return money less than we take, loss
                    journal_entry.append("accounts",
                                        {
                                            "account": row.from_treasury,
                                            "credit_in_account_currency": row.amount,
                                            "debit_in_account_currency": 0,
                                            "exchange_rate": row.last_exchange_rate
                                        }
                                        )

                    journal_entry.append("accounts",
                                        {
                                            "account": row.trading_treasury,
                                            "credit_in_account_currency": row.total,
                                            "debit_in_account_currency": 0,
                                            "exchange_rate": row.last_exchange_rate
                                        }
                                        )

                journal_entry.save()
                if type_of_je == "closing":
                    self.db_set("closing_journal_entry", journal_entry.name)
                    self.db_set("closed_by", frappe.session.user)
                frappe.db.commit()

        except Exception as e:
            print(e)
            traceback = frappe.get_traceback()
            frappe.log_error(
                title=_("Error while creating journal entry for {}".format(self.name)),
                message=traceback,
            )

    # create journal entry from data in Doc



    def validate(self):
        for rowx in self.exchange_table:
            rowx.total = rowx.amount

        names = frappe.get_list("Exchange Settings",{'employee':self.employee},['name'])
        # parents = frappe.db.sql(f"select name from `tabExchange Settings` where employee = '{self.employee}' ")
        if not names:
            frappe.throw(f'Please visit Exchange Settings and create a settings for employee {self.employee}')

    def on_change(self):
        for rowx in self.exchange_table:
            diff = flt(rowx.total) - flt(rowx.amount)
            frappe.db.set_value("Exchange Currency", rowx.name, "closing_differents_amount", diff)
        frappe.db.commit()

    def on_update_after_submit(self):
        if self.closed:
            frappe.throw("Clossed seesion, Not allow to trade")
        currency_total = {}
        for rowx in self.exchange_table:
            currency_total[rowx.currency] = rowx.total

        for row in self.daily_trading:
            if not row.processed:
                if row.from_currency == row.to_currency:
                    frappe.throw("Currency Change should have different currency not the same ")
                total = currency_total.get(row.from_currency)
                if row.from_amount > total:
                    frappe.throw(f"Row {row.idx} Amount {row.from_amount}  >  {total}  {row.from_currency}")
            
        for dt in self.daily_trading:
            if not dt.processed:
                for et in self.exchange_table:
                    if dt.from_currency == et.currency:
                        et_total = et.total - dt.from_amount
                        frappe.db.set_value("Exchange Currency", et.name, "total", et_total)
                    if dt.to_currency == et.currency:
                        et_total = et.total + dt.to_amount
                        frappe.db.set_value("Exchange Currency", et.name, "total", et_total)

                    if dt.from_currency != "LYD" and dt.to_currency == "LYD" and et.currency == dt.from_currency:
                        et_last_exchange_rate = dt.exchange_rate
                        frappe.db.set_value("Exchange Currency", et.name, "last_exchange_rate", et_last_exchange_rate)

                    elif dt.from_currency == "LYD" and dt.to_currency != "LYD" and et.currency == dt.to_currency:
                        et_last_exchange_rate = 1/dt.exchange_rate
                        frappe.db.set_value("Exchange Currency", et.name, "last_exchange_rate", et_last_exchange_rate)
                frappe.db.set_value("Exchange Table For Opening", dt.name, "processed", 1)

    def on_submit(self):
        open_exchange_journal_entry(self, self.exchange_table,
                                    type_of_je="opening")

    @frappe.whitelist()
    def close_exchange_journal_entry(self):
        close_exchange_journal_entry(self, self.exchange_table,
                                    type_of_je="closing")
        frappe.db.set_value(self.doctype, self.name, "closed", 1)
        return True

@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def query_fitler_for_account(doctype, txt, searchfield, start, page_len, filters):
    parents = frappe.db.sql(f"select name from `tabExchange Settings` where employee = '{filters['employee']}' ")
    return frappe.db.sql(
        """select currency 
        from `tabExchange Table` where 
        parent in %s and %s like %s order by currency  limit %s offset %s"""
        % ("%s", searchfield, "%s", "%s", "%s"),
        (parents[0], "%%%s%%" % txt, page_len, start),
        as_list=1,
    )

@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def query_fitler_for_account_trading_treasury(doctype, txt, searchfield, start, page_len, filters):
    parents = frappe.db.sql(f"select name from `tabExchange Settings` where employee = '{filters['employee']}' ")
    return frappe.db.sql(
        """select trading_treasury
        from `tabExchange Table` where currency = %s and
        parent in %s and %s like %s order by currency  limit %s offset %s"""
        % ("%s", "%s", searchfield, "%s", "%s", "%s"),
        (filters['currency'], parents[0], "%%%s%%" % txt, page_len, start),
        as_list=1,
    )

@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def query_fitler_for_account_from_treasury(doctype, txt, searchfield, start, page_len, filters):
    parents = frappe.db.sql(f"select name from `tabExchange Settings` where employee = '{filters['employee']}' ")
    return frappe.db.sql(
        """select from_treasury
        from `tabExchange Table` where currency = %s and
        parent in %s and %s like %s order by currency  limit %s offset %s"""
        % ("%s", "%s", searchfield, "%s", "%s", "%s"),
        (filters['currency'], parents[0], "%%%s%%" % txt, page_len, start),
        as_list=1,
    )


@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def query_fitler_for_account_profit_loss_treasury(doctype, txt, searchfield, start, page_len, filters):
    parents = frappe.db.sql(f"select name from `tabExchange Settings` where employee = '{filters['employee']}' ")
    return frappe.db.sql(
        """select profit_loss_treasury
        from `tabExchange Table` where currency = %s and
        parent in %s and %s like %s order by currency  limit %s offset %s"""
        % ("%s", "%s", searchfield, "%s", "%s", "%s"),
        (filters['currency'], parents[0], "%%%s%%" % txt, page_len, start),
        as_list=1,
    )

@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def query_fitler_for_account_exchange(doctype, txt, searchfield, start, page_len, filters):
    return frappe.db.sql(
        """select currency from `tabExchange Currency`
        where parent = %s and %s like %s order by name limit %s offset %s"""
        % ("%s", searchfield, "%s", "%s", "%s"),
        (filters["open_exchange_session"], "%%%s%%" % txt, page_len, start),
        as_list=1,
    )
