from microservices.utils import message
from database.database_adapter import DatabaseAdapter


class AssertiveCaseTest:
    def __init__(
        self,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.database = DatabaseAdapter()
        self.database_table = 'caso_teste_assertiva'

    def backup(self):
        is_success, details = self.database.query.select_all(
            self.database_table,
            columns='*'
        )

        if is_success:
            return message(200, {'projects': details})

        return message(500, f'Error on project retrive:\n{details}')

    def insert(self, payload):
        is_success, details = self.database.persistence.insert(
            self.database_table,
            total_casos_teste=payload.get('total_test_cases'),
            total_assertivas=payload.get('total_assertives'),
            quantidade_casos_teste=('test_cases_quantity'),
            assertivas=payload.get('assertives'),
            id_projeto=payload.get('project_id')
        )

        if is_success:
            return message(200, 'Success')

        return message(500, f'Error on project insert:\n{details}')

    def delete(self, payload):
        is_success, details = self.database.persistence.delete(
            self.database_table,
            id=payload.get('id')
        )

        if is_success:
            return message(200, 'Success')

        return message(500, f'Error on project delete:\n{details}')
