import sqlite3

import psycopg2
from psycopg2.extras import DictCursor

from load_data import load_from_sqlite


if __name__ == '__main__':
    dsl = {'dbname': 'movies_database', 'user': 'app', 'password': '123qwe',
           'host': '127.0.0.1', 'port': 5432}

    with sqlite3.connect('db.sqlite') as sqlite_conn, psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn:  # noqa
        load_from_sqlite(sqlite_conn, pg_conn)
