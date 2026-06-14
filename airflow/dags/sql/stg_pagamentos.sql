SELECT
    -- dimensoes
    p.id_cliente,
    p.dt_movimento,
    pp.tipo_pagamento,

    -- rastreamento
    p.id_pedido,

    -- metricas
    pp.nr_item_pagamento,
    pp.vl_transacao,
    pp.nr_parcelas_pagamento
FROM producao.pedidos p
JOIN producao.pedido_pagamento pp
ON p.id_pedido = pp.id_pedido