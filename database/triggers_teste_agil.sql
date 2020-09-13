-- ** MÉTRICAS DE TESTE ÁGIL E APOIO AO TESTE UNITÁRIO **

-- Calcula os fator de teste para atualizar o campo
-- **fator_teste** da tabela fator_teste
CREATE OR REPLACE FUNCTION calcula_fator_teste()
 RETURNS trigger
 LANGUAGE plpgsql
AS $function$
BEGIN
	IF
		pg_trigger_depth() < 2 AND
		NEW.total_linhas_teste IS NOT NULL AND
		NEW.total_linhas_producao IS NOT NULL
	THEN
		UPDATE fator_teste
		SET metrica = (
			SELECT ROUND( total_linhas_teste::numeric / total_linhas_producao, 2)
			FROM fator_teste
			WHERE id_projeto = NEW.id_projeto
		)
		WHERE id_projeto = NEW.id_projeto;
		UPDATE metricas
		SET fator_teste = (
			SELECT ROUND( total_linhas_teste::numeric / total_linhas_producao, 2)
			FROM fator_teste
			WHERE id_projeto = NEW.id_projeto
		)
		WHERE id_projeto = NEW.id_projeto;
	END IF;
	RETURN NEW;
END;
$function$;

CREATE TRIGGER calcula_fator_teste AFTER
UPDATE ON fator_teste FOR EACH ROW EXECUTE FUNCTION calcula_fator_teste();

-- Calcula a quantidade de caso de teste
-- para atualizar o campo **quantidade_casos_teste** da tabela caso_teste_assertiva

CREATE OR REPLACE FUNCTION calcula_casos_teste()
 RETURNS trigger
 LANGUAGE plpgsql
AS $function$
BEGIN
	IF
		pg_trigger_depth() < 2 AND
		NEW.total_casos_teste IS NOT NULL
	THEN
		UPDATE caso_teste_assertiva
		SET quantidade_casos_teste = ROUND(
			NEW.total_casos_teste::numeric / (
				SELECT total_linhas_producao
				FROM fator_teste
				WHERE id_projeto = NEW.id_projeto
			), 2
		)
		WHERE id_projeto = NEW.id_projeto;
		UPDATE metricas
		SET quantidade_casos_teste = ROUND(
			NEW.total_casos_teste::numeric / (
				SELECT total_linhas_producao
				FROM fator_teste
				WHERE id_projeto = NEW.id_projeto
			), 2
		)
		WHERE id_projeto = NEW.id_projeto;
	END IF;
	RETURN NEW;
END;
$function$;

CREATE TRIGGER calcula_casos_teste AFTER
UPDATE ON caso_teste_assertiva FOR EACH ROW EXECUTE FUNCTION calcula_casos_teste();

-- Calcula a quantidade de assertivas
-- para atualizar o campo **assertivas** da tabela caso_teste_assertiva

CREATE OR REPLACE FUNCTION calcula_assertivas()
 RETURNS trigger
 LANGUAGE plpgsql
AS $function$
BEGIN
	IF
		pg_trigger_depth() < 2 AND
		NEW.total_assertivas IS NOT NULL
	THEN
		UPDATE caso_teste_assertiva
		SET assertivas = ROUND(
			NEW.total_assertivas::numeric / (
				SELECT total_linhas_producao
				FROM fator_teste
				WHERE id_projeto = NEW.id_projeto
			), 2
		)
		WHERE id_projeto = NEW.id_projeto;
		UPDATE metricas
		SET assertivas = ROUND(
			NEW.total_assertivas::numeric / (
				SELECT total_linhas_producao
				FROM fator_teste
				WHERE id_projeto = NEW.id_projeto
			), 2
		)
		WHERE id_projeto = NEW.id_projeto;
	END IF;
	RETURN NEW;
END;
$function$;

CREATE TRIGGER calcula_assertivas AFTER
UPDATE ON caso_teste_assertiva FOR EACH ROW EXECUTE FUNCTION calcula_assertivas();

-- Calcula quantidade percentual de assertivas passando e falhando para atualizar
-- os campos **porcentagem_passando** e **porcentagem_falhando** da tabela porcentagem_assertivas

CREATE OR REPLACE FUNCTION calcula_porcentagem_assertivas()
 RETURNS trigger
 LANGUAGE plpgsql
AS $function$
BEGIN
	IF
		pg_trigger_depth() < 2
	THEN
		IF
			NEW.assertivas_passando IS NOT NULL
		THEN
			UPDATE porcentagem_assertivas
			SET porcentagem_passando = ROUND(
				NEW.assertivas_passando::numeric / (
					SELECT total_assertivas
					FROM caso_teste_assertiva
					WHERE id_projeto = NEW.id_projeto
				), 2
			)
			WHERE id_projeto = NEW.id_projeto;
			UPDATE metricas
			SET porcentagem_passando = ROUND(
				NEW.assertivas_passando::numeric / (
					SELECT total_assertivas
					FROM caso_teste_assertiva
					WHERE id_projeto = NEW.id_projeto
				), 2
			)
			WHERE id_projeto = NEW.id_projeto;
		END IF;
		IF
			NEW.assertivas_falhando IS NOT NULL
		THEN
			UPDATE porcentagem_assertivas
			SET porcentagem_falhando = ROUND(
				NEW.assertivas_falhando::numeric / (
					SELECT total_assertivas
					FROM caso_teste_assertiva
					WHERE id_projeto = NEW.id_projeto
				), 2
			)
			WHERE id_projeto = NEW.id_projeto;
			UPDATE metricas
			SET porcentagem_falhando = ROUND(
				NEW.assertivas_falhando::numeric / (
					SELECT total_assertivas
					FROM caso_teste_assertiva
					WHERE id_projeto = NEW.id_projeto
				), 2
			)
			WHERE id_projeto = NEW.id_projeto;
		END IF;
	END IF;
	RETURN NEW;
END;
$function$;

CREATE TRIGGER calcula_porcentagem_assertivas AFTER
UPDATE ON porcentagem_assertivas FOR EACH ROW EXECUTE FUNCTION calcula_porcentagem_assertivas();

-- Calcula a Quantidade de Testes de Aceitação por Funcionalidades para atualizar
-- o campo **numero_casos_aceitacao** da tabela aceitacao_funcionalidades

CREATE OR REPLACE FUNCTION calcula_casos_aceitacao()
 RETURNS trigger
 LANGUAGE plpgsql
AS $function$
BEGIN
	IF
		pg_trigger_depth() < 2 AND
		NEW.total_caso_teste IS NOT NULL AND
		NEW.total_caso_teste_anterior IS NOT NULL
	THEN
		UPDATE aceitacao_funcionalidades
		SET numero_casos_aceitacao = NEW.total_caso_teste - NEW.total_caso_teste_anterior
		WHERE id_projeto = NEW.id_projeto;
		UPDATE metricas
		SET numero_casos_aceitacao = NEW.total_caso_teste - NEW.total_caso_teste_anterior
		WHERE id_projeto = NEW.id_projeto;
	END IF;
	RETURN NEW;
END;
$function$;

CREATE TRIGGER calcula_casos_aceitacao AFTER
UPDATE ON aceitacao_funcionalidades FOR EACH ROW EXECUTE FUNCTION calcula_casos_aceitacao();

-- Calcula a Porcentagem de Assertivas de Teste de Aceitação Passando e Falhando para atualizar
-- os campos **assertivas_porcentagem_passando** e **assertivas_porcentagem_falhando** da tabela porcentagem_assertivas_aceitacao

CREATE OR REPLACE FUNCTION calcula_porcentagem_assertivas_aceitacao()
 RETURNS trigger
 LANGUAGE plpgsql
AS $function$
BEGIN
	IF
		pg_trigger_depth() < 2
	THEN
		IF
			NEW.assertivas_passando IS NOT NULL AND
			NEW.total_assertivas IS NOT NULL
		THEN
			UPDATE porcentagem_assertivas_aceitacao
			SET assertivas_porcentagem_passando = ROUND(
				NEW.assertivas_passando::numeric / (
					SELECT total_assertivas
					FROM porcentagem_assertivas_aceitacao
					WHERE id_projeto = NEW.id_projeto
				), 2
			)
			WHERE id_projeto = NEW.id_projeto;
			UPDATE metricas
			SET aceitacao_porcentagem_passando = ROUND(
				NEW.assertivas_passando::numeric / (
					SELECT total_assertivas
					FROM porcentagem_assertivas_aceitacao
					WHERE id_projeto = NEW.id_projeto
				), 2
			)
			WHERE id_projeto = NEW.id_projeto;
		END IF;
		IF
			NEW.assertivas_falhando IS NOT NULL AND
			NEW.total_assertivas IS NOT NULL
		THEN
			UPDATE porcentagem_assertivas_aceitacao
			SET assertivas_porcentagem_falhando = ROUND(
				NEW.assertivas_falhando::numeric / (
					SELECT total_assertivas
					FROM porcentagem_assertivas_aceitacao
					WHERE id_projeto = NEW.id_projeto
				), 2
			)
			WHERE id_projeto = NEW.id_projeto;
			UPDATE metricas
			SET aceitacao_porcentagem_falhando = ROUND (
				NEW.assertivas_falhando::numeric / (
					SELECT total_assertivas
					FROM porcentagem_assertivas_aceitacao
					WHERE id_projeto = NEW.id_projeto
				), 2
			)
			WHERE id_projeto = NEW.id_projeto;
		END IF;
	END IF;
	RETURN NEW;
END;
$function$;

CREATE TRIGGER calcula_porcentagem_assertivas_aceitacao AFTER
UPDATE ON porcentagem_assertivas_aceitacao FOR EACH ROW EXECUTE FUNCTION calcula_porcentagem_assertivas_aceitacao();