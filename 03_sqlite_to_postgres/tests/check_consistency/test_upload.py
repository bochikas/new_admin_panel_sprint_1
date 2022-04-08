import datetime
import os
import sqlite3
import sys

import psycopg2
import pytest
from dateutil.parser import parse
from psycopg2.extras import DictCursor

from models import FilmWork, Genre, GenreFilmWork, Person, PersonFilmWork
from load_data import get_fields

parent_dir_name = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
sys.path.append(parent_dir_name + "/check_consistency")

TABLES = {'film_work': FilmWork, 'person': Person, 'genre': Genre,
          'genre_film_work': GenreFilmWork, 'person_film_work': PersonFilmWork}
DB_PATH = '03_sqlite_to_postgres/db.sqlite'
DSL = {'dbname': 'movies_database', 'user': 'app', 'password': '123qwe',
       'host': '127.0.0.1', 'port': 5432}


def test_integrity():
    """Проверка соответствия количества записей в таблицах БД."""

    sqlite_count = 0
    postgre_count = 0
    with sqlite3.connect(f'{DB_PATH}') as sqlite_conn, psycopg2.connect(**DSL) as pg_conn:  # noqa
        for table in TABLES:
            curs = sqlite_conn.cursor()
            curs.execute(f"SELECT * FROM {table};")
            result = curs.fetchall()
            sqlite_count = len(result)

            cursor = pg_conn.cursor()
            cursor.execute(f'SELECT COUNT(*) FROM {table};', [])
            results = cursor.fetchone()
            postgre_count = results[0]

            assert sqlite_count == postgre_count, (
                f'Количество записей в таблице {table} не совпадает с источником'
            )
            sqlite_count = 0
            postgre_count = 0


def test_contents():
    """Проверка соответствия содержимого."""

    with sqlite3.connect(f'{DB_PATH}') as sqlite_conn, psycopg2.connect(**DSL, cursor_factory=DictCursor) as pg_conn:  # noqa
        for table in TABLES:
            _fields = get_fields(TABLES[table])

            sqlite_conn.row_factory = sqlite3.Row
            cursor = sqlite_conn.cursor()
            cursor.execute(f'SELECT {_fields} FROM {table};')
            sqlite_results = cursor.fetchall()

            curs = pg_conn.cursor()
            curs.execute(f'SELECT {_fields} FROM {table};')
            pg_results = curs.fetchmany(500)

            for _sqlt, _pg in zip(sqlite_results, pg_results):
                for field in _fields.split(', '):
                    _sqlt_data = getattr(TABLES[table](*_sqlt), field)
                    _pg_data = getattr(TABLES[table](*_pg), field)

                    msg = (f'Данные в поле {field}, таблицы {table} не '
                           'совпадают с источником')

                    if isinstance(_pg_data, datetime.datetime):
                        assert parse(_sqlt_data) == _pg_data, msg
                    else:
                        assert _sqlt_data == _pg_data, msg
