import os
import sqlite3
from typing import Dict, List, Any

DB_NAME = "obshak.db"
PAYMENTS_TABLE_NAME = "obshak"
conn = sqlite3.connect(os.path.join("db", DB_NAME))
cursor = conn.cursor()


def insert(table: str, column_values: Dict):
    columns = ', '.join(column_values.keys())
    values = [tuple(column_values.values())]
    placeholders = ", ".join("?" * len(column_values.keys()))
    cursor.executemany(
        f"INSERT INTO {table} "
        f"({columns}) "
        f"VALUES ({placeholders})",
        values)
    conn.commit()


def debts_get_info_by_id(id: int):
    cursor.execute(f'SELECT * FROM {PAYMENTS_TABLE_NAME} WHERE id = {id} ')
    rows = cursor.fetchall()
    if (rows == []):
        return ()
    return rows[0]


# if needed, we can do it flexible, but i am lazy(
def debts_update_amount(id: int, amount: int):
    print("SQL: Update amount of debt")
    cursor.execute(f"UPDATE {PAYMENTS_TABLE_NAME} SET amount={amount} WHERE id={id}")
    conn.commit()


# -1 means no query
def debts_search_by_users(creditor_id: str, debtor_id: str):
    cursor.execute(
        f"SELECT * FROM {PAYMENTS_TABLE_NAME} WHERE creditor_id ='{creditor_id}' AND debtor_id='{debtor_id}'")
    print(f"SQL: Execute command: search")
    ids = cursor.fetchall()
    if ids == []:
        print("SQL: Result: Not found record in db")
        return ()
    print(f"SQL: Result: Found id {ids[0][0]}")
    return ids[0]


def debts_search_debtors_by_creditor(creditor_id: str):
    cursor.execute(f"SELECT * FROM {PAYMENTS_TABLE_NAME} WHERE creditor_id ='{creditor_id}'  AND amount>0")
    print(
        f"SQL: Execute command: SELECT debtor_id, amount FROM {PAYMENTS_TABLE_NAME} WHERE creditor_id ='{creditor_id}' AND amount>0")
    debtors = cursor.fetchall()
    if not debtors:
        print("SQL: Result: Not found")
        return []
    print("SQL: Result: Found debtors")
    return debtors


def debts_search_creditors_by_debtor(debtor_id: str):
    cursor.execute(f"SELECT * FROM {PAYMENTS_TABLE_NAME} WHERE debtor_id ='{debtor_id}'  AND amount>0")
    print(f"SQL: Execute command: SELECT * FROM {PAYMENTS_TABLE_NAME} WHERE debtor_id ='{debtor_id}'  AND amount>0")
    ids = cursor.fetchall()
    if ids == []:
        print("SQL: Result: Not found")
        return []
    print("SQL: Result: Found creditors")
    return ids


def fetchall(table: str, columns: List[str]):
    columns_joined = ", ".join(columns)
    cursor.execute(f"SELECT {columns_joined} FROM {PAYMENTS_TABLE_NAME}")
    rows = cursor.fetchall()
    result = []
    for row in rows:
        dict_row = {}
        for index, column in enumerate(columns):
            dict_row[column] = row[index]
        result.append(dict_row)
    return result


def delete(table: str, row_id: int):
    row_id = int(row_id)
    cursor.execute(f"delete from {table} where id={row_id}")
    conn.commit()


def get_cursor():
    return cursor


def _init_db():
    """Инициализирует БД"""
    with open("createdb.sql", "r") as f:
        sql = f.read()
    cursor.executescript(sql)
    conn.commit()


def check_db_exists():
    """Проверяет, инициализирована ли БД, если нет — инициализирует"""
    try:
        cursor.execute("SELECT creditor_id FROM obshak")
    except:
        _init_db()
        print("Database is init\n")
    table_exists = cursor.fetchall()
    if table_exists:
        print("Database already exist\n")
        return
    # """Проверяет, инициализирована ли БД, если нет — инициализирует"""
    # cursor.execute(f"SELECT name FROM sqlite_master "
    #                "WHERE type='table' AND name='{PAYMENTS_TABLE_NAME}'")
    # table_exists = cursor.fetchall()
    # if table_exists == []:
    #     print("Database is ready\n")
    #     return
    # _init_db()
    # print("Database is created and ready\n")


check_db_exists()
