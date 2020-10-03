from microservices.utils import message
from database.database_adapter import DatabaseAdapter


class ProjectMeasure:
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
        is_success, details = self.database.persistence.insert(
            self.database_table,
            data_real_termino=payload.get('real_date_finish'),
            data_planejada_termino=payload.get('plan_date_finish'),
            data_real_inicio=payload.get('real_date_begin'),
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
