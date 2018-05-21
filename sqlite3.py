import sqlite3
from sqlite3 import Cursor
from typing import Tuple, Iterable

from .log import Log


class SQLite3:
    def __init__(self, db_name):
        self._sql_conn = sqlite3.connect(db_name)

    def execute(self, sql: str, parameters: Tuple=()) -> Cursor:
        c = self._sql_conn.cursor()
        return c.execute(sql, parameters)

    def executemany(self, sql: str, parameters: Iterable[Iterable]) -> Cursor:
        c = self._sql_conn.cursor()
        return c.executemany(sql, parameters)

    def create_table(self, table_name: str, columns: list, column_specs: list):
        if len(columns) != len(column_specs):
            Log.e('columns and column_specs do not match in length')
            return

        column_sql = ''
        for i in range(len(columns)):
            column_sql += "%s %s" % (columns[i], column_specs[i])
            if i + 1 < len(columns):
                column_sql += ", "
        sql = "create table %s (%s)" % (table_name, column_sql)
        self.execute(sql)
        self._sql_conn.commit()

    def commit(self):
        self._sql_conn.commit()

    def close(self):
        self._sql_conn.close()
