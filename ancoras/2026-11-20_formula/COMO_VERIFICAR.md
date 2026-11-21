# Como verificar a âncora (qualquer pessoa, sem confiar na Konfirmu)

1. Confirmar o hash do documento:
   `sha256sum A_FORMULA_ANTI_ALUCINACAO.md` → `7fde57a3fbe48d5a645fad387142da360a84c77fda1fab866ae7a7e039e25fb3`
2. Confirmar a âncora no Bitcoin (OpenTimestamps):
   - no browser: https://opentimestamps.org → largar o `.ots` e depois o documento;
   - ou no terminal: `pip install opentimestamps-client` e `ots verify A_FORMULA_ANTI_ALUCINACAO.md.ots`.

Carimbo enviado a 2026-11-20 11:48:00 UTC aos calendários Alice, Bob (opentimestamps.org) e Finney (eternitywall.com).
Estado em 20-11 15:25 UTC: CONFIRMADO no Bitcoin — Bloco Bitcoin 976 735 (txid 1998907025483895bcd4617f98c8ffe316268a6a46233b9f5e8c1b7e15a1d2fc, 20-11-2026 14:17:33 UTC) e bloco 976 737 (txid 013201050ba152921e155d704e01f5e2baa6e627c5b58dbf032f3c008ed0607b, 14:25:06 UTC). Raízes de Merkle conferidas com os cabeçalhos dos blocos (mempool.space). Finney ainda pendente; não faz falta.
O carimbo prova que este ficheiro existia naquela data. Não prova autoria nem que o conteúdo é verdadeiro.
