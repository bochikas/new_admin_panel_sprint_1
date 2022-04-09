import sqlite3
from dataclasses import fields

from psycopg2.extensions import connection as _connection
from psycopg2.extras import execute_batch

from models import FilmWork, Genre, GenreFilmWork, Person, PersonFilmWork

BATCH_SIZE = 50


def get_fields(model):
    """
    Получение всех полей в модели
    """
    _fields = list(field.name for field in fields(model))
    _fields = ', '.join(_fields)

    return _fields


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

        for line in data:
            temp_data = [model(*row) for row in line]

            _fields = get_fields(model)
            values = '%s ' * len(_fields.split())
            _values = ','.join(values.split())

            with self.connection.cursor() as cursor:
                query = (f'INSERT INTO content.{table_name} ({_fields}) '
                         f'VALUES ({_values}) ON CONFLICT (id) DO NOTHING')

                insert_data = list()
                row = list()

                for obj in temp_data:
                    for field in _fields.split(', '):
                        x = getattr(obj, field)
                        row.append(x)
                    insert_data.append(tuple(row))
                    row = []

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

        cursor = self.connection.cursor()

        fields = get_fields(model)

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
        while data:
            postgres_saver.save_all_data(data, model, table)
            break
