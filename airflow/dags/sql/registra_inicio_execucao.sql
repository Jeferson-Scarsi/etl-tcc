SET TIME ZONE 'america/sao_paulo';
INSERT INTO config.execucao_etl (ferramenta,
                                 run_id,
                                 inicio,
                                 status)
SELECT 'Apache Airflow' AS ferramenta,
       (
           SELECT COALESCE(MAX(run_id), 0) + 1
           FROM config.execucao_etl
           WHERE ferramenta = 'Apache Airflow'
       )             AS run_id,
       NOW()         AS inicio,
       'INICIADO'    AS status;