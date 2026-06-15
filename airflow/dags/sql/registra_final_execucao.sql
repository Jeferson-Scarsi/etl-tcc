SET TIME ZONE 'america/sao_paulo';
UPDATE config.execucao_etl
SET fim              = NOW(),
    duracao_segundos = EXTRACT(EPOCH FROM (NOW() - inicio)),
    status           = 'FINALIZADO'
WHERE run_id = (
                   SELECT MAX(run_id)
                   FROM config.execucao_etl
                   where ferramenta = 'Apache Airflow'
)
  AND ferramenta = 'Apache Airflow';