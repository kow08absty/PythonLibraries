import sqlite3
import os
from sqlite3 import Cursor
from typing import Tuple, Iterable

from .log import Log


class SQLite3:
    def __init__(self, db_name):
        if not os.path.isdir(os.path.dirname(db_name)):
            os.makedirs(os.path.dirname(db_name))
        self._sql_conn = sqlite3.connect(db_name)

    def cursor(self) -> Cursor:
        return self._sql_conn.cursor()

    def execute(self, sql: str, parameters: Tuple=()) -> Cursor:
        c = self.cursor()
        return c.execute(sql, parameters)

    def executemany(self, sql: str, parameters: Iterable[Iterable]) -> Cursor:
        c = self.cursor()
        return c.executemany(sql, parameters)

    def is_exists_table(self, table_name: str) -> bool:
        sql = 'select name from sqlite_master where type=\'table\' and name=\'{0}\''.format(
            table_name
        )
        c = self.execute(sql)
        return len(c.fetchall()) > 0

    def force_create_table(self, table_name: str, columns: list, column_specs: list):
        if self.is_exists_table(table_name):
            self.execute('drop table %s' % table_name)

        self.create_table_if_not_exists(table_name, columns, column_specs)

    def create_table_if_not_exists(self, table_name: str, columns: list, column_specs: list):
        if len(columns) != len(column_specs):
            Log.e('columns and column_specs do not match in length')
            return
        if self.is_exists_table(table_name):
            return

        column_sql = ''
        for i in range(len(columns)):
            column_sql += "%s %s" % (columns[i], column_specs[i])
            if i + 1 < len(columns):
                column_sql += ", "
        sql = "create table %s (%s)" % (table_name, column_sql)
        self.execute(sql)
        self.commit()

    def commit(self):
        self._sql_conn.commit()

    def close(self):
        self._sql_conn.close()
