import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class Query:
    def __init__(
            self,
            conn=None,
            *args,
            **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.connection = conn

    @staticmethod
    def list_to_words(columns, stringify=False):
        if columns[0] is '*':
            is_more_one_column = True
            return columns[0], is_more_one_column

        # Casting list to words comma separated
        is_more_one_column = len(columns) > 1

        if is_more_one_column:
            columns = [
                f"'{value}'" if stringify else value
                for value in columns
            ]
            return ', '.join(columns), is_more_one_column

        column = f"'{columns[0]}'" if stringify else columns[0]

        return column, is_more_one_column

    def select_all(self, table, columns):
        """ Select all rows from chosen table and columns
        :param table: (str) table that query will made
        :param columns: (list) columns chosen to table query
        :return: list contaning query result
        """
        columns, is_more_one_column = self.list_to_words(columns)

        try:
            sql = f"""
                SELECT {columns}
                FROM {table}
            """

            self.connection.cursor.execute(sql)

            if is_more_one_column:
                return True, self.connection.cursor.fetchall()

            return True, [row[0] for row in self.connection.cursor]

        except Exception as message:
            logging.info(f'Error on query:\n{message}')
            return False, message
