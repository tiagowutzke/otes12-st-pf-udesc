import logging

from database.query import Query

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class Persistence:
    def __init__(
        self,
        conn=None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.connection = conn

    def insert(self, table, **cols_values):
        query = Query()

        print(list(cols_values.keys()))
        print(list(cols_values.values()))

        columns, _ = query.list_to_words(list(cols_values.keys()))
        values, _ = query.list_to_words(list(cols_values.values()), stringify=True)

        try:
            sql = f"""
                INSERT INTO {table} ({columns})
                VALUES ({values})
            """
            print(sql)
            self.connection.commit_transaction(sql)
            return True, ''

        except Exception as e:
            message = f'Error on insert values:\n{e}'
            logging.info(message)
            return False, message

    def delete(self, table, id):
        try:
            sql = f"""
                DELETE FROM {table}
                WHERE id = {id}
            """
            self.connection.commit_transaction(sql)
            return True, ''

        except Exception as e:
            message = f'Error on insert values:\n{e}'
            logging.info(message)
            return False, message
