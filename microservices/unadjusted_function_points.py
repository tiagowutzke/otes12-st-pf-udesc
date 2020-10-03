from microservices.utils import message
from database.database_adapter import DatabaseAdapter


class UnadjustedFunctionPoints:
    def __init__(
        self,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.database = DatabaseAdapter()
        self.database_table = 'pontos_funcao_n_ajustados'

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
            complexidade=payload.get('complex'),
            arquivo_logico_interno=payload.get('internal_logic_file'),
            arquivo_interface_externa=payload.get('external_interface_file'),
            entradas_externas=payload.get('external_inputs'),
            saidas_externas=payload.get('external_outputs'),
            consultas_externas=payload.get('external_queries'),
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
