-- ** PREPARAÇÃO DAS MÉTRICAS **

-- Quando um novo projeto é inserido, o gatilho fará a inserção do registro do projeto
-- em cada tabela de métricas
CREATE OR REPLACE FUNCTION prepara_metricas_projeto()
 RETURNS trigger
 LANGUAGE plpgsql
AS $function$
DECLARE
	tabela varchar;
	tabelas_array varchar[] := array[
		'pontos_funcao',
		'medidas_projeto'
	];
BEGIN
	IF
		pg_trigger_depth() < 2
	THEN
		FOREACH tabela IN ARRAY tabelas_array
	   	LOOP
	   		EXECUTE
	   			'INSERT INTO ' || tabela || '(id_projeto)'
				'VALUES (' || NEW.id || ')';
	   	END LOOP;
	END IF;
	RETURN NEW;
END;
$function$;


CREATE TRIGGER prepara_metricas_projeto AFTER
INSERT ON projetos FOR EACH ROW EXECUTE FUNCTION prepara_metricas_projeto();

-- ** MEDIDAS DE PROJETO **

-- Calcula a metrica de medidas de projeto quando há
-- mudança de registros na tabela
CREATE OR REPLACE FUNCTION calcula_medidas_projeto()
 RETURNS trigger
 LANGUAGE plpgsql
AS $function$
BEGIN
	IF
		pg_trigger_depth() < 2 AND
		NEW.data_real_termino IS NOT NULL AND
		NEW.data_planejada_termino IS NOT NULL AND
		NEW.data_real_inicio IS NOT NULL
	THEN
		UPDATE medidas_projeto
		SET metrica = ROUND(
			(
				SELECT (data_real_termino - data_planejada_termino)::numeric * 100 / (data_planejada_termino - data_real_inicio)
				FROM medidas_projeto mp
				WHERE id = NEW.id
			)
		, 2)
		WHERE id = NEW.id;
	END IF;
	RETURN NEW;
END;
$function$;

CREATE TRIGGER calcula_medidas_projeto AFTER
INSERT OR UPDATE ON medidas_projeto FOR EACH ROW EXECUTE FUNCTION calcula_medidas_projeto();

-- ** PONTOS POR FUNÇÃO **

-- Calcula o total de fatores de caracteristicas gerais do sistema para
-- atualizar o campo **gsc** da tabela pontos_funcao
CREATE OR REPLACE FUNCTION calcula_gsc()
 RETURNS trigger
 LANGUAGE plpgsql
AS $function$
BEGIN
	IF
		pg_trigger_depth() < 2
	THEN
		UPDATE pontos_funcao
		SET gsc = (
			SELECT
				comunicacao_dados +
				proc_dados_distribuido +
				performance +
				uso_sistema +
				taxa_transacoes +
				entrada_dados_online +
				eficiencia_usuario_final +
				atualizacao_online +
				processamento_complexo +
				reusabilidade +
				facilidade_instalacao +
				facilidade_operacao +
				multiplos_locais +
				facilidade_mudanca
			FROM caracteristicas_gerais_sistema
			WHERE NEW.id_projeto = pontos_funcao.id_projeto
		)
		WHERE id = NEW.id;
	END IF;
	RETURN NEW;
END;
$function$;

CREATE TRIGGER calcula_gsc AFTER
INSERT OR UPDATE ON caracteristicas_gerais_sistema FOR EACH ROW EXECUTE FUNCTION calcula_gsc();
