from microservices.utils import message
from database.database_adapter import DatabaseAdapter


class FunctionPoints:
    def __init__(
        self,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.database = DatabaseAdapter()
        self.database_table = 'medidas_projeto'

    def backup(self):
        is_success, details = self.database.query.select_all(
            self.database_table,
            columns='*'
        )

        if is_success:
            return message(200, {'projects': details})

        return message(500, f'Error on project retrive:\n{details}')

    def insert(self, payload):
        """This data is result from other tables data. No insert needed"""
        pass

    def delete(self, payload):
        is_success, details = self.database.persistence.delete(
            self.database_table,
            id=payload.get('id')
        )

        if is_success:
            return message(200, 'Success')

        return message(500, f'Error on project delete:\n{details}')
