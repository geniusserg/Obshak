import datetime
import re
import exceptions
from model.debt_model import Debtor, Message
from payments.debts_db import DebtsDatabase

debts_db = DebtsDatabase()


class Obshak:
    def __init__(self):
        pass

    def add_debtor(self, cred_id, debt_id, amount, msg):
        debts_db.add_debtor(Debtor(cred_id, debt_id, amount, datetime.datetime.now(), msg))

    def get_creditors(self, user_id):
        return debts_db.get_creditors(user_id)

    def get_debtors(self, user_id):
        return debts_db.get_debtors(user_id)

    def pay(self, user_id):
        print(debts_db.get_creditors(user_id))

    def process_message(self, raw_message, creditor_id):
        """Парсит текст пришедшего сообщения о новом расходе."""
        print(raw_message)
        regexp_result = []
        try:
            # Регулярка выделяет id и сумму должника в сообщении.
            regexp_result = re.findall(r"(\d*)\|@\w+] (\d+)", raw_message)
        except AttributeError:
            print('Я не понял, сори(')
        if not regexp_result:
            raise exceptions.NotCorrectMessage(
                "Не могу понять сообщение. Напишите сообщение в формате, "
                "например:\n@username 500р")
        else:
            people = []
            amount = []
            text2 = []
            text = ''
            for i in regexp_result:
                text += 'ФИО:' + i[0] + ' Сумма:' + i[1] + '\n'
                text2.append('ФИО:' + i[0] + ' Сумма:' + i[1] + '\n')
                people.append(i[0])
                amount.append(i[1])
        return Message(creditor_id, people, amount, text, text2)


def add_testdata_db():
    creditors = [96221730]
    for i in creditors:
        debts_db.add_debtor(Debtor(i, 123, 400, datetime.datetime.now(), 'test_msg1'))
        debts_db.add_debtor(Debtor(i, 456, 500, datetime.datetime.now(), 'test_msg2'))
        debts_db.add_debtor(Debtor(123, i, 200, datetime.datetime.now(), 'test_msg3'))
        debts_db.add_debtor(Debtor(456, i, 300, datetime.datetime.now(), 'test_msg4'))
