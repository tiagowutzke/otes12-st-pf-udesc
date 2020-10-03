from microservices.utils import message
from database.database_adapter import DatabaseAdapter


class Project:
    def __init__(
        self,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.database = DatabaseAdapter()
        self.database_table = 'projetos'

    def backup(self):
        is_success, details = self.database.query.select_all(
            table=self.database_table,
            columns='*'
        )

        if is_success:
            return message(200, {'projects': details})

        return message(500, f'Error on project retrive:\n{details}')

    def insert(self, payload):
        is_success, details = self.database.persistence.insert(
            table=self.database_table,
            descricao=payload.get('description')
        )

        if is_success:
            return message(200, 'Success')

        return message(500, f'Error on project insert:\n{details}')

    def delete(self, payload):
        is_success, details = self.database.persistence.delete(
            table=self.database_table,
            id=payload.get('id')
        )

        if is_success:
            return message(200, 'Success')

        return message(500, f'Error on project delete:\n{details}')
