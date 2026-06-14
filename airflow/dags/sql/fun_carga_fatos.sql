SELECT dw.fun_carga_fato_vendas();
SELECT dw.fun_carga_fato_pagamentos();
UPDATE config.contador SET nr_contador = nr_contador + 1 WHERE desc_contador = 'contador_execucao';