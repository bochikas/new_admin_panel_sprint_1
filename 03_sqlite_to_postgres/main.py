import sqlite3

import psycopg2
from psycopg2.extras import DictCursor
from psycopg2.extensions import connection as _connection

from loader import SQLiteLoader
from models import FilmWork, Genre, GenreFilmWork, Person, PersonFilmWork
from saver import PostgresSaver

BATCH_SIZE = 50


def main(connection: sqlite3.Connection, pg_conn: _connection):
    """
    Основной метод загрузки данных из SQLite в Postgres
    """

    postgres_saver = PostgresSaver(pg_conn, BATCH_SIZE)
    sqlite_loader = SQLiteLoader(connection, BATCH_SIZE)

    tables = {
        'film_work': FilmWork, 'person': Person, 'genre': Genre,
        'genre_film_work': GenreFilmWork, 'person_film_work': PersonFilmWork
    }

    for table, model in tables.items():
        data = sqlite_loader.load_movies(table, model)
        postgres_saver.save_all_data(data, model, table)


if __name__ == '__main__':
    dsn = {'dbname': 'movies_database', 'user': 'app', 'password': '123qwe',
           'host': '127.0.0.1', 'port': 5432}

    with sqlite3.connect('db.sqlite') as sqlite_conn, psycopg2.connect(**dsn, cursor_factory=DictCursor) as pg_conn:  # noqa
        main(sqlite_conn, pg_conn)
