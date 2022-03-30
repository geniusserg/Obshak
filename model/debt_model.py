import datetime
from typing import NamedTuple, Optional


class Debtor(NamedTuple):
    cred_id:   Optional[int]
    debt_id:   Optional[int]
    amount:    int
    date_time: datetime.datetime
    raw_text:  str


class Message():
    def __init__(self, creditor, people, amount):
        self.creditor=creditor
        self.people = people
        self.amount = amount
        self.people_username = None
    def generate_message(self):
        text = ""
        for i in  range(len(self.people)):
            text += 'Пользователь: @id' + str(self.people_username[id][0]['id'])\
             + ' (' + self.people_username[id] + " "\
             + self.people_username[id][0]['last_name'] + ") " \
             + '. Сумма: ' + self.amount[id] + "\n"
        return text
    def generate_message(self, id: int):
        return 'Пользователь: @id' + str(self.people_username[id][0]['id'])\
             + ' (' + self.people_username[id][0]['first_name'] + " "\
             + self.people_username[id][0]['last_name'] + ") " \
             + '. Сумма: ' + self.amount[id] + "\n"