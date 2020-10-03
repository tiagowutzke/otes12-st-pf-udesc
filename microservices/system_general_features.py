from microservices.utils import message
from database.database_adapter import DatabaseAdapter


class SystemGerenalFeatures:
    def __init__(
        self,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.database = DatabaseAdapter()
        self.database_table = 'caracteristicas_gerais_sistema'

    def backup(self):
        is_success, details = self.database.query.select_all(
            self.database_table,
            columns='*'
        )

        if is_success:
            return message(200, {'projects': details})

        return message(500, f'Error on project retrive:\n{details}')

    def insert(self, payload):
        payload = payload.get('payload')

        is_success, details = self.database.persistence.insert(
            self.database_table,
            comunicacao_dados=payload.get('data_comunication'),
            proc_dados_distribuido=payload.get('data_distribution'),
            performance=payload.get('performance'),
            uso_sistema=payload.get('system_use'),
            taxa_transacoes=payload.get('transaction_rate'),
            entrada_dados_online=payload.get('online_data_in'),
            eficiencia_usuario_final=payload.get('user_efficiency'),
            atualizacao_online=payload.get('online_update'),
            processamento_complexo=payload.get('complex_processing'),
            reusabilidade=payload.get('reusability'),
            facilidade_instalacao=payload.get('set_up_difficult'),
            facilidade_operacao=payload.get('operation_difficult'),
            multiplos_locais=payload.get('multiple_locals'),
            facilidade_mudanca=payload.get('change_difficult'),
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
