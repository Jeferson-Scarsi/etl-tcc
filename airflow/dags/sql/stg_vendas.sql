SELECT
    -- dimensoes
    p.id_cliente,
    pi.id_produto,
    pi.id_vendedor,
    p.status_pedido,

    -- rastreamento
    p.id_pedido,
    pi.id_item_pedido,

    -- metricas
    pi.vl_movimento,
    pi.vl_movimento_frete,

    -- datas
    p.dt_movimento::date as dt_movimento,
    p.dt_aprovacao,
    p.dt_entrega_cliente
FROM producao.pedidos p
JOIN producao.pedido_item pi
ON p.id_pedido = pi.id_pedido;