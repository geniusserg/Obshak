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
    text:     str
    text2:    list
