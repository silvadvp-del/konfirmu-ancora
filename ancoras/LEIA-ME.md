# Âncoras — segunda âncora, em git

Autor: David Peres da Silva.

Estas pastas têm cópias byte a byte de documentos já ancorados no Bitcoin com OpenTimestamps.
Este repositório público é a segunda âncora: junta a data deste commit à data do Bitcoin.

*EN: byte-for-byte copies of documents already anchored in Bitcoin with OpenTimestamps. This public repository is a second, independent anchor.*

| Pasta | Documento | SHA-256 do documento | Bitcoin |
|---|---|---|---|
| `2026-11-20_formula/` | A FÓRMULA ANTI-ALUCINAÇÃO | `7fde57a3fbe48d5a645fad387142da360a84c77fda1fab866ae7a7e039e25fb3` | blocos 976 735 (txid `1998907025483895bcd4617f98c8ffe316268a6a46233b9f5e8c1b7e15a1d2fc`) e 976 737 (txid `013201050ba152921e155d704e01f5e2baa6e627c5b58dbf032f3c008ed0607b`), 20-11-2026 |
| `2026-11-20_kcp-0.1/` | KCP/0.1 — Konfirmu Claim Protocol | `3090f6c700053dcedad78747f2f28575e9e86eed4cb6de30c81d5c7a0254ca44` | os mesmos blocos 976 735 e 976 737, 20-11-2026 |
| `2026-11-21_kcp-0.2/` | KCP/0.2 «O Perfil da Paz» — revisão com pontos `[VALIDAR]` ainda abertos | `0da8e6e244a369e49f2bd15249f6d1d87d58c0ed1411089da13ed1a5fec61f53` | bloco 976 803 (txid `f67c585314655212523112a9f230198337e0a600c22c0f97ce2c3b2fc66517d2` e `adac1414a233b3e9561e597f3151c04a6b675e3d5bb37253ab8c412a188a0d76`), 21-11-2026, 00:10:59 UTC |

## Como verificar, sem confiar em ninguém

1. Em cada pasta: `sha256sum -c SHA256SUMS*` (no Mac: `shasum -a 256 -c SHA256SUMS*`).
2. A data: `ots verify <ficheiro>.ots` com o cliente OpenTimestamps, ou em https://opentimestamps.org largar o `.ots` e depois o ficheiro.
3. Os blocos: o cabeçalho de cada bloco está em qualquer explorador público (por exemplo mempool.space); a raiz de Merkle tem de bater com a que o `.ots` dá.

Cada documento tem o seu `.ots`. Nas pastas do KCP há também o `.ots` da lista `SHA256SUMS_*`, que carimba todos os ficheiros que essa lista nomeia.

## O que isto não garante

Prova que estes ficheiros existiam nessas datas e que não mudaram desde então.
Não prova que o conteúdo está certo e não substitui o julgamento humano.

Cada documento mantém a licença que traz no próprio texto.

Espelho na web: https://konfirmu-verificar.vercel.app/formula.html · https://konfirmu-verificar.vercel.app/kcp.html · https://konfirmu-verificar.vercel.app/kcp/KCP-0.2.md
