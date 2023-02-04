import os
import MySQLdb
from MySQLdb.cursors import Cursor
from typing import Union, Optional


class DBConnection:

    def __get_connection():

        host = "db"
        user = os.getenv("MARIADB_USER")
        passwd = os.getenv("MARIADB_PASSWORD")
        db = os.getenv("MARIADB_DATABASE")
        port = 3306
        charset = "utf8"

        connection: MySQLdb.Connection = MySQLdb.connect(
            host=host,
            user=user,
            passwd=passwd,
            db=db,
            port=port,
            charset=charset)
        return connection

    def __init__(self, auto_commit: bool = True) -> None:
        self.conn = DBConnection.__get_connection()
        self.auto_commit = auto_commit

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.auto_commit and exc_type is None:
            self.commit()
        self.close()

    def commit(self):
        """
        コミットを明示的に実行します
        """
        self.conn.commit()

    def close(self):
        """
        接続をcloseします
        """
        self.conn.close()

    def execute(self, sql: str, *, values: Optional[tuple] = None) -> Cursor:
        """
        SQLを実行します
        主に戻り値を受け取らない場合に利用
        """
        cursor: Cursor = self.conn.cursor()
        cursor.execute(sql, args=values)
        return cursor

    def select(self, sql: str, values: Optional[Union[list, tuple]] = None):
        """
        SQLを実行し結果をTupleで受け取ります
        """
        cursor = self.execute(sql=sql, values=values)
        rows: tuple[tuple] = cursor.fetchall()
        return rows

    def insert(self, table: str, *, ignore: bool = False, columns: str = None,  values: Union[list[Union[list, tuple]], tuple[Union[tuple, list]]]):
        """
        insert文を実行します
        """
        ignore_str = "ignore " if ignore else ""
        column = len(values[0])
        row = len(values)
        value_str = ",".join(["%s" for _ in range(column)])
        value_str = ",".join([f"({value_str})" for _ in range(row)])

        if columns == None:
            sql = f"insert {ignore_str}into {table} values{value_str}"
        else:
            sql = f"insert {ignore_str}into {table}({columns}) values{value_str}"
        self.execute(
            sql=sql,
            values=(val for sub in values for val in sub),
        )

    def last_insert_id(self) -> int:
        """
        insert文で最後に入力したIDを取得します
        Auto incrimentに設定されてない場合取得できません
        """
        cursor = self.execute("select last_insert_id()")
        return cursor.fetchone()[0]
