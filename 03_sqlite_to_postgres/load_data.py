import sqlite3
from dataclasses import fields, astuple

from psycopg2.extensions import connection as _connection
from psycopg2.extras import execute_batch

from models import FilmWork, Genre, GenreFilmWork, Person, PersonFilmWork

BATCH_SIZE = 50


def get_fields(model):
    """
    Получение всех полей модели в виде списка
    """

    fields_lst = list(field.name for field in fields(model))
    return fields_lst


def get_fields_str(model):
    """
    Получение всех полей модели в виде строки
    """

    fields_str = ', '.join(get_fields(model))
    return fields_str


class PostgresSaver:
    """
    Запись данных в PostgreSQL
    """

    def __init__(self, connection):
        self.connection = connection

    def save_all_data(self, data, model, table_name):
        """
        Метод записи данных в базу
        """

        fields_str = get_fields_str(model)
        fields = get_fields(model)

        values = ','.join(['%s'] * len(fields))

        for batch in data:
            insert_data = [astuple(model(*row)) for row in batch]

            with self.connection.cursor() as cursor:
                query = (f'INSERT INTO content.{table_name} ({fields_str}) '
                         f'VALUES ({values}) ON CONFLICT (id) DO NOTHING')

                execute_batch(cursor, query, insert_data, page_size=BATCH_SIZE)
                self.connection.commit()


class SQLiteLoader:
    """
    Обработка данных из базы SQLite
    """

    def __init__(self, connection):
        self.connection = connection
        self.connection.row_factory = sqlite3.Row

    def load_movies(self, table, model):
        """
        Получение данных из базы SQLite
        """

        fields = get_fields_str(model)

        cursor = self.connection.cursor()
        cursor.execute(f'SELECT {fields} FROM {table};')
        data = cursor.fetchmany(BATCH_SIZE)

        while data:
            yield data
            data = cursor.fetchmany(BATCH_SIZE)


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection):
    """
    Основной метод загрузки данных из SQLite в Postgres
    """

    postgres_saver = PostgresSaver(pg_conn)
    sqlite_loader = SQLiteLoader(connection)

    tables = {
        'film_work': FilmWork, 'person': Person, 'genre': Genre,
        'genre_film_work': GenreFilmWork, 'person_film_work': PersonFilmWork
    }

    for table, model in tables.items():
        data = sqlite_loader.load_movies(table, model)
        postgres_saver.save_all_data(data, model, table)
