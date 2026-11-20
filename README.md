# KONFIRMU / FABLE OS — Genesis Seal & Verification Kit

Infraestrutura europeia onde a IA propõe e o humano confirma, com selo de
proveniência e selo de frescura. Este repositório é o **selo de génese** do
projecto: os bytes canónicos do `GENESIS_STAMP_v4.json`, os hashes verificados
byte a byte e as instruções para qualquer pessoa re-executar a verificação.

> O_QUE_NAO_GARANTE: Mathematical truth supports human justice; it never
> replaces human conscience or judicial accountability. Um hash interno prova
> integridade dos bytes — autoria e data provam-se com o timestamp externo
> (OpenTimestamps `.ots` + DOI Zenodo), não com o hash.

## Os selos (verificados 2026-11-20, sessão lead — saída colada em `VERIFICACAO-SAIDA.txt`)

| Objecto | Valor |
|---|---|
| Ficheiro `GENESIS_STAMP_v4.json` (bytes brutos, 1885 B) | sha256 `3cfe80002b756a40b81ceeae1ff5bec58d55bc49b80303f94cb16164ac036277` |
| Bytes canónicos do `genesis_record` (1339 B, sort_keys, separadores `(",":":")`, `ensure_ascii=False`) | sha256 `3bb318dd28742a435a11032a6a00cb4103fe4b40666a9251b91c3ef253fd9296` |
| shake256 (512 bits) dos mesmos bytes | `cedc5dce6eb2d9ca01b1ad0c15ef6929f9dc619a261bf4588ff534ce81ad2847763ffe36c27778386952f0009e7bc48e53dd2bcd444f4300ab7a9ffe7d77a034` |
| Manifesto de hashes | ver `MANIFESTO_HASHES_2026-11-20.txt` |
| Timestamp blockchain | `GENESIS_STAMP_v4.json.ots` + `MANIFESTO_HASHES_2026-11-20.txt.ots` (verificar com `ots verify`) |

## Verificar você mesmo (0 dependências além de Python stdlib)

```sh
python3 verificacao.py          # recalcula tudo e confere os selos
shasum -a 256 -c SHA256SUMS.txt # confere cada ficheiro deste repo
ots verify GENESIS_STAMP_v4.json.ots    # confere o timestamp (cliente OpenTimestamps)
```

## Honestidade registada (histórico da casa)

Um hash anunciado em conversa (`538f2ca5…`) foi **predito por texto e não
executado** — a confissão e a verificação que o provou estão documentadas em
`VERIFICACAO-SAIDA.txt` (0 de 8 variantes de serialização produzem esse
prefixo). O hash verdadeiro é o da tabela acima. Regra da casa: nenhum hash
viaja sem o ficheiro que o produziu.

## Licença

EUPL-1.2 (ver `LICENSE`). © 2026 Casa Konfirmu.

[![License: EUPL-1.2](https://img.shields.io/badge/License-EUPL--1.2-blue.svg)](https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12)
[![DOI](https://zenodo.org/badge/DOI/PLACEHOLDER.svg)](https://doi.org/PLACEHOLDER)
