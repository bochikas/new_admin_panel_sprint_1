import sqlite3

from utils import get_fields_str


class SQLiteLoader:
    """
    Обработка данных из базы SQLite
    """

    def __init__(self, connection, batch_size):
        self.connection = connection
        self.connection.row_factory = sqlite3.Row
        self.batch_size = batch_size

    def load_movies(self, table, model):
        """
        Получение данных из базы SQLite
        """

        fields = get_fields_str(model)

        cursor = self.connection.cursor()
        cursor.execute(f'SELECT {fields} FROM {table};')
        data = cursor.fetchmany(self.batch_size)

        while data:
            yield data
            data = cursor.fetchmany(self.batch_size)
