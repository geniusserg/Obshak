import datetime
from typing import NamedTuple, Optional


class Debtor(NamedTuple):
    cred_id:   Optional[int]
    debt_id:   Optional[int]
    amount:    int
    date_time: datetime.datetime
    raw_text:  str


class Message(NamedTuple):
    creditor: Optional[int]
    people:   list
    amount:   list
    def generate_message(self):
        text = ""
        for i in  range(len(self.people)):
            text += 'Пользователь: ' + self.people[i] + ' Сумма: ' + self.amount[i] + '\n'
        return text
    def generate_message(self, id: int):
        return 'Пользователь: @id' + str(self.people[id][0]['id'])\
             + ' (' + self.people[id][0]['first_name'] + " "\
             + self.people[id][0]['last_name'] + ") " \
             + '. Сумма: ' + self.amount[id] + "\n"