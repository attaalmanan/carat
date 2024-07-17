import frappe
import json
from datetime import date
from frappe import _, msgprint
from frappe.utils import cint, today, flt


def make_journal_entry_closing(self, debit, credit, main_treasury,
                                                damaged_cash_treasury='', holding_treasury='',
                                                  transaction_type="deposit"):
    try:
        customer = self.customer
        if transaction_type == "transfer":
            customer = self.to
        # total_amount = flt(self.amount) - flt(commission_amount)
        total_amount = flt(self.amount)
        journal_entry = frappe.new_doc("Journal Entry")
        journal_entry.posting_date = today()
        journal_entry.user_remark = self.name
        # journal_entry.custom_created_from = self.name or ""
        if (self.currency != frappe.defaults.get_user_default("currency")):
            journal_entry.multi_currency = 1
        if self.amount != 0 and debit and credit:
            if (transaction_type == "deposit"):
                second_count_diff = flt(self.total_approved_amount) - total_amount
                credit_d = debit_d = 0
                if second_count_diff > 0:
                    debit_d = second_count_diff
                else:
                    credit_d = second_count_diff*-1
                journal_entry.append("accounts",
                                    {
                                        "account": debit,
                                        "exchange_rate": self.exchange_rate,
                                        "credit_in_account_currency": total_amount,
                                        "debit_in_account_currency": 0
                                    }
                                    )

                journal_entry.append("accounts",
                                    {
                                        "account": main_treasury,
                                        "exchange_rate": self.exchange_rate,
                                        "credit_in_account_currency": 0,
                                        "debit_in_account_currency": total_amount
                                    }
                                    )
                if credit_d != 0 or debit_d != 0:
                    journal_entry.append("accounts",
                                            {
                                                "account": credit,
                                                "party_type": "Customer",
                                                "party": customer,
                                                "exchange_rate": self.exchange_rate,
                                                "credit_in_account_currency":debit_d,
                                                "debit_in_account_currency":credit_d,
                                                }
                                            )
                    journal_entry.append("accounts",
                                        {
                                            "account": main_treasury,
                                            "exchange_rate": self.exchange_rate,
                                            "credit_in_account_currency":credit_d,
                                            "debit_in_account_currency":debit_d
                                        }
                                        )

                if self.total_damaged > 0:
                    journal_entry.append("accounts",
                                            {
                                                "account": damaged_cash_treasury,
                                                "party_type": "Customer",
                                                "party": customer,
                                                "exchange_rate":self.exchange_rate,
                                                "credit_in_account_currency": 0,
                                                "debit_in_account_currency": self.total_damaged,
                                            }
                                            )
                    journal_entry.append("accounts",
                                    {
                                        "account": main_treasury,
                                        "exchange_rate": self.exchange_rate,
                                        "credit_in_account_currency": self.total_damaged,
                                        "debit_in_account_currency": 0
                                    }
                                    )


                    journal_entry.append("accounts",
                                            {
                                                "account": holding_treasury,
                                                # "party_type": "Customer",
                                                # "party": customer,
                                                "exchange_rate": self.exchange_rate,
                                                "credit_in_account_currency": 0,
                                                "debit_in_account_currency": self.total_damaged,
                                            }
                                        )
                    journal_entry.append("accounts",
                                            {
                                                "account": credit,
                                                "party_type": "Customer",
                                                "party": customer,
                                                "exchange_rate": self.exchange_rate,
                                                "credit_in_account_currency":self.total_damaged,
                                                "debit_in_account_currency":0,
                                                }
                                            )


    
            elif (transaction_type == "withdraw"):
                journal_entry.append("accounts",
                                    {
                                        "account": debit,
                                        "exchange_rate": self.exchange_rate,
                                        "credit_in_account_currency": 0,
                                        "debit_in_account_currency": total_amount
                                    }
                                    )

                journal_entry.append("accounts",
                                    {
                                        "account": main_treasury,
                                        "exchange_rate": self.exchange_rate,
                                        "credit_in_account_currency": self.total_approved_amount,
                                        "debit_in_account_currency": 0
                                    }
                                    )
                journal_entry.append("accounts",
                                        {
                                            "account": damaged_cash_treasury,
                                            "exchange_rate":self.exchange_rate,
                                            "credit_in_account_currency": self.total_damaged,
                                            "debit_in_account_currency":0,
                                        }
                                        )
                journal_entry.append("accounts",
                                        {
                                            "account": credit,
                                            "party_type": "Customer",
                                            "party": customer,
                                            "exchange_rate": self.exchange_rate,
                                            "credit_in_account_currency": self.total_damaged,
                                            "debit_in_account_currency": 0,
                                        }
                                        )
                journal_entry.append("accounts",
                                        {
                                            "account": holding_treasury,
                                            "party_type": "Customer",
                                            "party": customer,
                                            "exchange_rate": self.exchange_rate,
                                            "credit_in_account_currency": 0,
                                            "debit_in_account_currency": flt(self.total_approved_amount) - total_amount,
                                        }
                                        )

            journal_entry.save()
            self.db_set("closing_journal_entry", journal_entry.name)
            self.db_set("closed_by", frappe.session.user)
            # self.save()
            # frappe.db.commit()
    except Exception as e:
        print(e)
        traceback = frappe.get_traceback()
        frappe.log_error(
            title=_("Error while creating journal entry  for {} - {} -{} -{}".format(self.name,total_amount,self.total_approved_amount, self.total_damaged)),
            message=traceback,
        )
        # frappe.db.rollback()
        self.db_set("workflow_state", "Received")


# create journal entry from data in Doc
def make_journal_entry(self, debit, credit, commission_account, commission_amount, transaction_type):
    try:
        customer = self.customer
        if transaction_type == "transfer":
            customer = self.to
        total_amount = flt(self.amount)
        journal_entry = frappe.new_doc("Journal Entry")
        journal_entry.posting_date = today()
        journal_entry.user_remark = self.name
        if (self.currency != frappe.defaults.get_user_default("currency")):
            journal_entry.multi_currency = 1
        if self.amount != 0 and debit and credit:
            journal_entry.append("accounts",
                                 {
                                     "account": debit,
                                     "exchange_rate": self.exchange_rate,
                                     "credit_in_account_currency": 0,
                                     "debit_in_account_currency": total_amount,
                                 }
                                 )

            journal_entry.append("accounts",
                                 {
                                     "account": credit,
                                     "party_type": "Customer",
                                     "party": customer,
                                     "exchange_rate": self.exchange_rate,
                                     "credit_in_account_currency": total_amount,
                                     "debit_in_account_currency": 0
                                 }
                                 )
            if (commission_amount):
                if (transaction_type == "deposit"):
                    journal_entry.append("accounts",
                                         {
                                             "account": credit, "party_type": "Customer",
                                             "party": self.customer,
                                             "exchange_rate":self.exchange_rate,
                                             "credit_in_account_currency": 0,
                                             "debit_in_account_currency": flt(commission_amount),
                                         }
                                         )
                elif (transaction_type == "withdraw"):
                    journal_entry.append("accounts",
                                         {
                                             "account": debit, "party_type": "Customer",
                                             "party": self.customer,
                                             "exchange_rate": self.exchange_rate,
                                             "credit_in_account_currency": 0,
                                             "debit_in_account_currency": flt(commission_amount),
                                         }
                                         )
                elif (transaction_type == "transfer"):
                    journal_entry.append("accounts",
                                         {
                                             "account": debit, "party_type": "Customer",
                                             "party": self.customer,
                                             "exchange_rate": self.exchange_rate,
                                             "credit_in_account_currency": 0,
                                             "debit_in_account_currency": flt(commission_amount),
                                         }
                                         )
                journal_entry.append("accounts",
                                     {
                                         "account": commission_account,
                                         "exchange_rate": self.exchange_rate,
                                         "credit_in_account_currency": flt(commission_amount),
                                         "debit_in_account_currency": 0,
                                     }
                                     )

            journal_entry.save()
            self.db_set("journal_entry", journal_entry.name)
            self.db_set("created_by", frappe.session.user)
            self.save()
            frappe.db.commit()

    except Exception as e:
        print(e)
        traceback = frappe.get_traceback()
        frappe.log_error(
            title=_("Error while creating journal entry for {}".format(self.name)),
            message=traceback,
        )

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
def open_exchange_journal_entry(self, exchange_table, type_of_je):
    try:
        journal_entry = frappe.new_doc("Journal Entry")
        journal_entry.posting_date = today()
        journal_entry.user_remark = self.name
        journal_entry.multi_currency = 1
        exchange_rate = ""
        for row in exchange_table:
            if type_of_je == "closing":
                exchange_rate = row.last_exchange_rate
                amount = row.total
            else:
                exchange_rate = row.exchange_rate
                amount = row.amount
            if amount != 0:
                journal_entry.append("accounts",
                                     {
                                         "account": row.from_treasury,
                                         "credit_in_account_currency": amount,
                                         "debit_in_account_currency": 0,
                                         "exchange_rate":   exchange_rate

                                     }
                                     )

                journal_entry.append("accounts",
                                     {
                                         "account": row.trading_treasury,
                                         "credit_in_account_currency": 0,
                                         "debit_in_account_currency": amount,
                                         "exchange_rate": exchange_rate


                                     }
                                     )

            journal_entry.save()
            if type_of_je == "closing":
                self.db_set("closing_journal_entry", journal_entry.name)
                self.db_set("closed_by", frappe.session.user)
            else:
                self.db_set("journal_entry", journal_entry.name)
                self.db_set("created_by", frappe.session.user)

            frappe.db.commit()

    except Exception as e:
        print(e)
        traceback = frappe.get_traceback()
        frappe.log_error(
            title=_("Error while creating journal entry for {}".format(self.name)),
            message=traceback,
        )


# create journal entry from data in Doc
def exchange_journal_entry(self, from_debit, from_amount, from_exchange_rate,
                           to_credit, to_amount, to_exchange_rate):
    try:
        journal_entry = frappe.new_doc("Journal Entry")
        journal_entry.posting_date = today()
        journal_entry.user_remark = self.name
        journal_entry.multi_currency = 1
        if from_amount != 0 and to_amount != 0:
            journal_entry.append("accounts",
                                 {
                                     "account": from_debit,
                                     "party_type": "Employee",
                                     "party": self.employee,
                                     "credit_in_account_currency": 0,
                                     "exchange_rate": from_exchange_rate,
                                     "debit_in_account_currency": from_amount,
                                 }
                                 )

            journal_entry.append("accounts",
                                 {
                                     "account": to_credit,
                                     "party_type": "Employee",
                                     "party": self.employee,
                                     "credit_in_account_currency": to_amount,
                                     "exchange_rate": to_exchange_rate,
                                     "debit_in_account_currency": 0
                                 }
                                 )

            journal_entry.save()
            self.db_set("journal_entry", journal_entry.name)
            self.db_set("created_by", frappe.session.user)
            frappe.db.commit()

    except Exception as e:
        print(e)
        traceback = frappe.get_traceback()
        frappe.log_error(
            title=_("Error while creating journal entry for {}".format(self.name)),
            message=traceback,
        )


@frappe.whitelist()
def get_active_session():
    employee = frappe.get_list("Employee", {"user_id": frappe.session.user})
    if employee:
        active = frappe.get_list("Open Exchange Session",
                                 {"employee": employee[0].name,
                                  "closed": 0}
                                 )
        if active:
            active_session = active[0].name
            doc = frappe.get_doc("Open Exchange Session", active_session)
            allowed_currency = []
            currency_symbol = {}
            for row in doc.exchange_table:
                allowed_currency.append(row.currency)
                currency_symbol[row.currency] = frappe.get_value("Currency",
                                                                 row.currency,
                                                                 "symbol")
            return {"allowed_currency": allowed_currency,
                    "employee": doc.employee_name,
                    "currency_symbol": currency_symbol}