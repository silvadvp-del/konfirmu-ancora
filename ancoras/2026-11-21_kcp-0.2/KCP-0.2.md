Autor da disciplina: David Peres da Silva · 21-11-2026 · prior art declarada

# KCP/0.2 — Konfirmu Claim Protocol · «O Perfil da Paz»

**Preâmbulo (PT).** Revisão normativa do KCP/0.1. A 0.1 fica em vigor por inteiro; a 0.2 junta-lhe quatro cláusulas (7 a 10).
Ordem do fundador de 21-11-2026, 00:40. «Sem prova verificável, não aconteceu.»

**Status:** defensive publication. Licence: EUPL-1.2. Author: David Peres da Silva. Anyone may implement KCP royalty-free.
**Base document:** `KCP_0.1.md`, SHA-256 `3090f6c700053dcedad78747f2f28575e9e86eed4cb6de30c81d5c7a0254ca44`,
anchored in Bitcoin blocks 976735 and 976737.
**Keywords:** MUST, MUST NOT, SHOULD, MAY as in RFC 2119 / RFC 8174.
**Marker:** `[VALIDAR]` = open point; not normative until the founder closes it.

## 0. Conformance and compatibility

0.1. A CLAIM under this revision carries `"kcp":"0.2"`.
0.2. A PROOF valid under KCP/0.1 remains valid. A 0.2 verifier MUST accept 0.1 seals.
0.3. KCP-JSON (0.1 §3), PROOF (0.1 §4) and the VERIFY steps (0.1 §5) are unchanged.
0.4. An implementation is KCP/0.2-conformant only if it satisfies Rules 1–10.

## 1. Rules 1–6 (inherited from KCP/0.1)

`[VALIDAR]` KCP/0.1 has eight sections and no numbered «hard rules». The six below are derived from its text.

1. **Mandatory limits.** Every CLAIM MUST carry a non-empty `o_que_nao_garante` (0.1 §2).
2. **One canonical form.** Bytes `C` MUST be produced by KCP-JSON (0.1 §3).
3. **Seal over the bytes.** `sig` MUST be pure Ed25519 (RFC 8032) over `C`, not over the hash (0.1 §4).
4. **Verification outside the AI.** VERIFY MUST be executable by a third party without the issuer's cooperation (0.1 §5).
5. **Failure is never «false».** Any failure MUST yield `NÃO VERIFICADO`; `SEM_COBERTURA` MUST NOT be read as false (0.1 §5).
6. **Small-order refusal.** A verifier MUST reject small-order points in `pub` and in `R` (0.1 §5.4).

## 7. Clause 7 — The Keys of the World (structural neutrality)

**7.1 Normative text**
7.1.1. The protocol has no operational owner.
7.1.2. Six chambers are defined, with these exact identifiers:
`AFRICA` · `EUROPE` · `ASIA` · `AMERICAS` · `CIVIL_SOCIETY` · `SCIENCE`.
7.1.3. The protocol root key MUST be generated in a key ceremony and split among the chambers. No single party,
including the original issuer, may hold a reconstructing set of shares.
7.1.4. An amendment to this specification is valid only if approved by a quorum of at least 4 of the 6 chambers.
The approval MUST be a KCP CLAIM carrying the SHA-256 of the amended text and one PROOF per approving chamber.
7.1.5. The original issuer MUST NOT amend the specification alone.
7.1.6. Issuer keys (0.1 §4) are unaffected: each issuer keeps signing its own CLAIMs with its own key.

`[VALIDAR]` Threshold: the order says «3-de-5» for the ceremony and names six chambers; Delta 3 says «3-de-5 → 4-de-6».
This text assumes 4-of-6 for both the key and amendments.
`[VALIDAR]` Scope of the root key: assumed to sign specification releases and chamber records only, never individual CLAIMs.
`[VALIDAR]` Transitional rule: until the genesis ceremony, who may issue revisions (0.2 itself is issued by the author).
`[VALIDAR]` How a chamber is constituted, who holds its share, and how a share is rotated or revoked.

**7.2 Founding case.** Genesis ceremony held in Maputo, Mozambique, before public launch.
`[VALIDAR]` «Public launch» needs a definition: KCP/0.1 is already published.

**7.3 o_que_nao_garante.** Does not guarantee that a chamber is representative, honest or independent. Does not prevent
collusion of four chambers. Does not create a legal entity. Does not protect a share that its holder leaks.

## 8. Clause 8 — The Right to Verify (Geneva symmetry)

**8.1 Normative text**
8.1.1. VERIFY is a right of the protocol: free of charge, unlimited in number, available to any party.
8.1.2. Verification MUST be symmetric. Two parties, including adversaries, verifying the same CLAIM and PROOF
MUST obtain the same result. An implementation MUST NOT serve a different result, rule set or key list by party.
8.1.3. An issuer MAY charge for producing a CLAIM. An issuer MUST NOT charge for, meter, rate-limit or gate VERIFY.
8.1.4. VERIFY MUST be executable offline, on the verifier's machine, with only: the CLAIM, the PROOF and the issuer's
public key. The issuer's private key MUST NOT be needed.
8.1.5. SLA: one VERIFY MUST complete in under 1 second on the reference hardware class.
8.1.6. A public key needed for VERIFY MUST be obtainable without authentication or payment.

`[VALIDAR]` Reference hardware class for 8.1.5 is undefined. Measured (§13): 3.9 ms CPU per VERIFY, pure-Python reference,
x86_64 server. Not yet measured on a low-end phone.
`[VALIDAR]` Rate limits on hosted convenience endpoints (e.g. 60/h on `/v1/verificar`): assumed allowed because local
VERIFY stays unlimited; confirm.

**8.2 Founding case.** Two opposing parties verify the same sealed fact and obtain the same bytes and the same answer.

**8.3 o_que_nao_garante.** Does not guarantee that the sealed fact is true, only that it is what the issuer sealed.
Does not guarantee access to the CLAIM itself. Does not guarantee that a party will accept the result.

## 9. Clause 9 — Truth with Mercy (profile KCP-RECONCILIATION)

**9.1 Normative text**
9.1.1. KCP-RECONCILIATION is an OPTIONAL profile. A CLAIM using it carries `"profile":"KCP-RECONCILIATION"`.
9.1.2. **Verified confession.** A party declares facts with proof. The CLAIM is sealed under 0.1 §4. Its state is `SEALED`.
A `SEALED` confession is permanent: its bytes and hash MUST NOT be altered or deleted by the protocol.
9.1.3. **Sealed archive.** After a reconciliation process, the chambers MAY issue a reconciliation record. The record is a
KCP CLAIM carrying: the hash of each confession covered, `agreement_sha256` (SHA-256 of the agreement text) and one PROOF
per approving chamber, at least 4 of 6.
9.1.4. **State machine.** States: `SEALED`, `RECONCILED`. The only transition is `SEALED → RECONCILED`. It is valid only
with a record conforming to 9.1.3. There is no transition out of `RECONCILED`.
9.1.5. In state `RECONCILED`: the fact and its hash remain verifiable under Clause 8. A conformant implementation
MUST NOT open, accept or seal a new accusation under this profile for facts covered by the record.
9.1.6. A verifier MUST report the state together with the VERIFY result.

`[VALIDAR]` What validates the «reconciliation process» before the chambers vote (parties, victims, mediator).
`[VALIDAR]` Whether victims hold a veto, and how it is recorded.
`[VALIDAR]` Irreversibility of 9.1.4 if the agreement is later shown to rest on a false confession.
`[VALIDAR]` Interaction with national and international law on acts that cannot be amnestied; outside this document.

**9.2 Founding case.** `[VALIDAR]` None supplied in the order.

**9.3 o_que_nao_garante.** Binds only conformant implementations of this profile. Does not bind any court, state or
person. Is not an amnesty in law. Does not erase the fact. Does not certify that the confession is complete or sincere.

## 10. Clause 10 — Declared Footprint

**10.1 Normative text**
10.1.1. Every KCP operation MUST declare its footprint in a `footprint` member of the response.
10.1.2. Form: `{"gco2e": number, "water_ml": number, "method": string, "basis": "measured" | "estimated"}`.
Numbers follow KCP-JSON number rules (0.1 §3).
10.1.3. For issuer operations (CLAIM + PROOF), `footprint` is a member of the CLAIM and is covered by `C`.
10.1.4. For VERIFY, `footprint` is a member of the result object produced by the verifier's implementation.
10.1.5. An implementation that omits `footprint`, or emits it without `method` and `basis`, is NON-CONFORMANT.
10.1.6. Reference target: about 1.7 gCO2e per verification.

`[VALIDAR]` Origin of the 1.7 gCO2e figure: no measurement record was found. Measured local VERIFY (§13): about
0.0000043 gCO2e under declared assumptions, i.e. about 395 000 times below 1.7 g. The 1.7 g figure cannot describe a
local VERIFY; it may describe a full hosted call with a model. The founder must say which operation it refers to.
`[VALIDAR]` No reference target was given for `water_ml`.
`[VALIDAR]` 10.1.3 changes `C` for 0.2 CLAIMs; 0.1 seals have no `footprint` and stay valid under 0.2.

**10.2 Founding case.** Reference target of about 1.7 gCO2e per verification `[VALIDAR]`.

**10.3 o_que_nao_garante.** Does not guarantee that the declared value is accurate; it is a self-declaration under
the issuer's seal. Does not reduce the footprint. Does not cover the hardware's manufacture unless `method` says so.

## 11. Code deltas (listed, not implemented)

| # | Delta | Where | Notes |
|---|---|---|---|
| D1 | Mandatory `footprint` in VERIFY | `konfirmu_calc.py` v2.5.1: `selar()` (issuer side), `selo_ok()` (result object) | New conformance vector: response without `footprint` → NON-CONFORMANT. `selo_ok()` returns a boolean today (confirmed); 10.1.4 needs a result object. |
| D2 | State machine `SEALED → RECONCILED` | P6, extended | New record type (9.1.3), quorum check ≥4 of 6, state reported with VERIFY. Confirmed: P6 in v2.5.1 is the escrow table `CONGELADO_15D → {CORRIGIDO, TRIBUNAL, EXPIRACAO_ESTORNO_ORIGEM}`; it has no `RECONCILIADO`. D2 is a second table, not an edit of the first. `[VALIDAR]` state names in code: PT (`SELADO`, `RECONCILIADO`) or EN. |
| D3 | Chamber ceremony format | Shamir 3-of-5 → 4-of-6 | Share labels = the six chamber identifiers of 7.1.2. `REGRAS["shamir"]` is `{k:3, n:5}` today (confirmed). `shamir_partir(…, 4, 6, …)` already works unchanged (§13). Old 3-of-5 vectors kept as legacy. |

Version bumps implied: `kcp` field `"0.2"`; new vector file `kcp_vetores_0.2.json`.

## 12. Destination

Same as 0.1: OpenTimestamps anchor and public mirror BEFORE any announcement.

## 13. Measurements (informative)

Run with the reference `konfirmu_calc.py` v2.5.1 (SHA-256 `7b0680f795d9614bf6de97dae507db3b21d61f99742753ef444565d0b32086a6`),
unmodified, script `medir_02.py`, output `medicoes_02.json`. Python 3.13, x86_64.

| Item | Result |
|---|---|
| VERIFY of a `"kcp":"0.2"` CLAIM carrying `footprint` | 20 of 20 accepted; tampered copy rejected |
| CPU time per VERIFY (20 distinct CLAIMs) | 0.003871 s — under the 1 s SLA of 8.1.5 |
| Footprint per local VERIFY | 0.0387 J → 0.0000043 gCO2e. ASSUMED: 10 W, 400 gCO2e/kWh |
| Shamir 4-of-6, labels of 7.1.2 | 15 of 15 quartets rebuild the key; 0 of 20 trios do |
| `RECONCILIADO` present in v2.5.1 | no |

o_que_nao_garante: one machine, one run; power and grid intensity are assumptions, not measurements; no water figure.
