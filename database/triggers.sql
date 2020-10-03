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
		'metricas',
		'fator_teste',
		'caso_teste_assertiva',
		'porcentagem_assertivas',
		'aceitacao_funcionalidades',
		'porcentagem_assertivas_aceitacao',
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
				FROM medidas_projeto
				WHERE id = NEW.id
			)
		, 2)
		WHERE id = NEW.id;
		UPDATE metricas
		SET medidas_projeto = ROUND(
			(
				SELECT (data_real_termino - data_planejada_termino)::numeric * 100 / (data_planejada_termino - data_real_inicio)
				FROM medidas_projeto
				WHERE id = NEW.id
			)
		, 2)
		WHERE id_projeto = NEW.id_projeto;
	END IF;
	RETURN NEW;
END;
$function$;

-- ** PONTOS POR FUNÇÃO **

-- Calcula o total de fatores de caracteristicas gerais do sistema para
-- atualizar o campo **gsc** da tabela pontos_funcao
-- ...
-- Calcula o fator de ajuste da função para atualizar o campo **vaf**
-- da tabela pontos_funcao
CREATE OR REPLACE FUNCTION calcula_gsc_vaf()
 RETURNS trigger
 LANGUAGE plpgsql
AS $function$
BEGIN
	IF
		pg_trigger_depth() < 2
	THEN
		-- GSC
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
			LIMIT 1
		)
		WHERE id_projeto = NEW.id_projeto;
		-- VAF
		UPDATE pontos_funcao
		SET vaf = ROUND(
			(
				SELECT 0.65 + (0.01 * gsc)
				FROM pontos_funcao
				WHERE id_projeto = NEW.id_projeto
			)
		, 2)
		WHERE id_projeto = NEW.id_projeto;
	END IF;
	RETURN NEW;
END;
$function$;

CREATE TRIGGER calcula_gsc_vaf AFTER
UPDATE or insert ON caracteristicas_gerais_sistema FOR EACH ROW EXECUTE FUNCTION calcula_gsc_vaf();

-- Calcula os pontos de função não ajustados para atualizar o campo
-- **ufp** da tabela pontos_funcao
CREATE OR REPLACE FUNCTION calcula_ufp()
 RETURNS trigger
 LANGUAGE plpgsql
AS $function$
BEGIN
	IF
		pg_trigger_depth() < 2
	THEN
		UPDATE pontos_funcao
		SET ufp = (
			SELECT
				sum(arquivo_logico_interno) +
				sum(arquivo_interface_externa) +
				sum(entradas_externas) +
				sum(saidas_externas) +
				sum(consultas_externas)
			FROM pontos_funcao_n_ajustados
			WHERE id_projeto = NEW.id_projeto
		)
		WHERE id_projeto = NEW.id_projeto;
	END IF;
	RETURN NEW;
END;
$function$;

-- Calcula os pontos de função ajustados para atualizar o campo
-- **afp** da tabela pontos_funcao
CREATE TRIGGER calcula_ufp AFTER
UPDATE OR INSERT ON pontos_funcao_n_ajustados FOR EACH ROW EXECUTE FUNCTION calcula_ufp();

CREATE OR REPLACE FUNCTION calcula_afp()
 RETURNS trigger
 LANGUAGE plpgsql
AS $function$
BEGIN
	IF
		pg_trigger_depth() < 2
	THEN
		UPDATE pontos_funcao
		SET afp = ufp * vaf
		WHERE id_projeto = NEW.id_projeto;
		UPDATE metricas
		SET pontos_funcao = (
			SELECT afp
			FROM pontos_funcao
			WHERE id_projeto = NEW.id_projeto
		)
		WHERE id_projeto = NEW.id_projeto;
	END IF;
	RETURN NEW;
END;
$function$;

CREATE TRIGGER a_calcula_afp AFTER
UPDATE OR INSERT ON pontos_funcao_n_ajustados FOR EACH ROW EXECUTE FUNCTION calcula_afp();

CREATE TRIGGER b_calcula_afp AFTER
UPDATE OR INSERT ON caracteristicas_gerais_sistema FOR EACH ROW EXECUTE FUNCTION calcula_afp();

