Autor da disciplina: David Peres da Silva · 20-11-2026 · prior art declarada

# KCP/0.1 — Konfirmu Claim Protocol: CLAIM → PROOF → VERIFY

*Abstract (EN): KCP is an open protocol in which every factual claim produced by an AI carries its own proof: a canonical JSON
object, its SHA-256 hash and an Ed25519 signature (RFC 8032) over the canonical bytes. Verification runs outside the AI, locally,
in milliseconds. Published as a defensive publication: anyone may implement it, royalty-free.*

**Estado:** publicação defensiva. Texto CC BY 4.0 · implementações EUPL-1.2. Qualquer pessoa pode implementar o KCP sem pedir
licença nem pagar. O que se declara aqui é a disciplina e a combinação; as peças de base são de outros e ficam creditadas:
Ed25519 (RFC 8032), SHA-256 (FIPS 180-4), modelo de credenciais verificáveis do W3C (VC 2.0).

## 1. Papéis
**Emissor** afirma e carimba. **Portador** guarda e mostra. **Verificador** confere — fora da IA, sem pedir licença a ninguém.

## 2. CLAIM (a afirmação)
Objeto JSON com, pelo menos: `kcp` (`"0.1"`), `emissor`, `emitido_em` (UTC, ISO 8601), `veredicto`
(`VERIFICADO` · `DIVERGE_DA_FICHA` · `SEM_COBERTURA`), `o_que_nao_garante` (obrigatório, nunca vazio) e, quando há fonte,
`facto_selado` = `{id, facto, fonte, data, nao_garante, hash}` com `hash = SHA-256(KCP-JSON({id, facto, fonte, data, nao_garante}))`.
O texto de quem pergunta pode ir só como `afirmacao_sha256` (o emissor não precisa de o guardar).

## 3. KCP-JSON (forma canónica)
UTF-8 sem escapes ASCII · chaves ordenadas por ponto de código · sem espaços (`,` e `:`) · texto em NFC antes de selar ·
números reais arredondados a 12 algarismos significativos (`0.1+0.2` → `0.3`) · NaN e infinito proibidos · bytes em hexadecimal.
**Não é** o JCS (RFC 8785): a regra dos números é outra. Chama-se `C` aos bytes resultantes.

## 4. PROOF (o selo)
`{"alg":"Ed25519+SHA-256", "hash": hex(SHA-256(C)), "pub": hex(chave pública, 32 bytes), "sig": hex(Ed25519(sk, C))}`.
A assinatura é Ed25519 puro (RFC 8032) sobre os bytes `C`, não sobre o hash. O hash serve para conferir depressa e para ancorar.

## 5. VERIFY (fora da IA)
1. Recalcular `C` a partir do CLAIM recebido; 2. comparar `SHA-256(C)` com `hash` em tempo constante;
3. confirmar que `pub` é uma chave aceite (publicada pelo emissor, p. ex. `GET /v1/chave`, ou fixada pelo verificador);
4. verificar a assinatura segundo o RFC 8032, recusando pontos de ordem pequena em `pub` e em `R`;
5. qualquer falha → **NÃO VERIFICADO**. Nunca «falso»: `SEM_COBERTURA` também não quer dizer falso.

## 6. Alinhamento
**RFC 8032:** o selo de referência é aceite byte a byte por uma implementação independente (OpenSSL) e reproduz o vetor oficial
§7.1 TEST 1. **W3C VC 2.0:** emissor ↔ `issuer`, CLAIM ↔ `credentialSubject`, selo ↔ `proof`. Diferença declarada: a forma
canónica é própria, por isso um selo KCP/0.1 **não** é um `DataIntegrityProof` `eddsa-jcs-2022`. A ponte fica para o KCP/0.2.

## 7. Referência e vetores
Implementação de referência: `konfirmu_calc.py` v2.5.1 (SHA-256 `7b0680f795d9614bf6de97dae507db3b21d61f99742753ef444565d0b32086a6`),
demo **147/147** (saída SHA-256 `147bace57c892e16347981e593c458b45c974101eae4db30ef5545ddc8e39dc7`). A v2.8 (serviço público
`/v1/verificar`, `/v1/facto`) junta a NFC e a recusa de ordem pequena; com texto em NFC, as duas dão os mesmos bytes.
Vetores: `kcp_vetores_0.1.json` (chave de teste pública, CLAIM, `C`, selo, caso negativo).

## 8. O que não garante
Garante proveniência e integridade: «idêntico ao que o emissor selou, na data em que selou». Não garante que a fonte tenha
razão, não prova quem é a pessoa por trás de uma chave sem a publicação dessa chave, e não substitui o julgamento humano.
