from dataclasses import astuple

from psycopg2.extras import execute_batch

from utils import get_fields, get_fields_str


class PostgresSaver:
    """
    Запись данных в PostgreSQL
    """

    def __init__(self, connection, batch_size):
        self.connection = connection
        self.batch_size = batch_size

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

                execute_batch(cursor, query, insert_data, page_size=self.batch_size)
                self.connection.commit()