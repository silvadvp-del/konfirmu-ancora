#!/usr/bin/env python3
# VERIFICAÇÃO BYTE-A-BYTE (sessão lead, 2026-11-20) — stdlib-only.
# Recalcula os selos do genesis a partir dos bytes reais e confere contra:
#   (a) o hash "predito" 538f2ca5... confessado como não-executado;
#   (b) o ficheiro GENESIS_STAMP_v4.json depositado na workspace;
#   (c) o manifesto MANIFESTO_HASHES_2026-11-20.txt.
import hashlib
import json

CLAIMED_PREDICTED = "538f2ca5867a8a3beee6c9c1c19ed63088d7c0b7a6aa3f2385966a35e9d8e530"

# 1) genesis_record EXACTAMENTE como consta na mensagem do Maestro (script do paste).
genesis_record = {
    "axioms": [
        "P1_GUM_CORRELATED_METROLOGY",
        "P2_THERMODYNAMIC_AND_QUANTUM_VETO",
        "P3_HYBRID_PQC_SHAKE512_ED25519",
        "P4_APPEND_ONLY_DETERMINISTIC_LEDGER",
        "P5_SHAMIR_3_OF_5_NONCE_SINGLE_USE",
        "P6_POLICY_ZERO_15D_FREEZE_HUMAN_TRIBUNAL",
        "P7_VERSIONED_FORMULAS_MEDIDO_VS_ASSUMIDO",
        "P8_LOTKA_VOLTERRA_HOMEOSTASIS",
        "P9_ANTI_SYBIL_COMMUNITY_QUORUM_K5",
        "P10_COMPLETE_CRYPTOGRAPHIC_LINEAGE",
        "P11_INVERSE_BOTTLENECK_ELASTICITY",
        "P12_TRIANGULATED_ORACLES_N3_UNCERTAINTY_BRAKE_85",
        "P13_ANTI_GOODHART_MAD_BAND",
        "P14_VITAL_VALVE_AND_2PCT_WORKER_REPAIR_FUND",
        "P15_PONTO_NEUTRAL_ONE_HEALTH_PLANETARY_BOUNDARIES",
    ],
    "domains_verified": [
        "ENERGY_SOLAR_MICROGRIDS",
        "QUANTUM_SAFE_FINANCE_AND_TRADE",
        "CIRCULAR_DEADSTOCK_AND_EWASTE",
        "GLOBAL_SHIPPING_DCSA_HAZMAT_OFFSHORE",
        "COOPERATIVE_ROBOTICS_SAFETY_KERNEL",
        "SOVEREIGN_MEDICINE_AND_COLD_CHAIN",
        "BIOCLIMATIC_HOUSING_AND_VERIFIED_WORK",
        "DIRECT_CREATOR_CULTURE_AND_YOUTH_SPORT",
        "FRUGAL_COMPUTING_AND_OPEN_SCIENCE",
    ],
    "honesty_boundary": "O_QUE_NAO_GARANTE: Mathematical truth supports human justice; it never replaces human conscience or judicial accountability.",
    "license": "EUPL-1.2",
    "mote": "Vamos recomeçar, mas desta vez bem feito.",
    "origin_coordinates": "Hückelhoven/NRW (EU) <-> Geneva/Zug (CH) <-> Sovereign Africa",
    "project": "KONFIRMU / FABLE OS",
    "timestamp_utc": "2026-11-20T09:20:00Z",
    "version": "v4.0-GENESIS-SEALED",
}

canonical_bytes = json.dumps(
    genesis_record, sort_keys=True, separators=(",", ":"), ensure_ascii=False
).encode("utf-8")
true_sha256 = hashlib.sha256(canonical_bytes).hexdigest()
true_shake = hashlib.shake_256(canonical_bytes).hexdigest(64)

print("== PASSO 1: hash verdadeiro do genesis_record do paste ==")
print("CANONICAL_BYTES_LEN :", len(canonical_bytes))
print("TRUE_SHA256         :", true_sha256)
print("TRUE_SHAKE256_512BIT:", true_shake)
print("MATCHES_CLAIMED_538f2ca5:", true_sha256 == CLAIMED_PREDICTED)

print()
print("== PASSO 2: 8 variantes de serialização plausíveis — alguma começa por 538f2ca5? ==")
variants = []
for sk in (True, False):
    for ea in (True, False):
        for sep in (None, (",", ":")):
            b = json.dumps(genesis_record, sort_keys=sk, separators=sep, ensure_ascii=ea).encode("utf-8")
            variants.append((f"sort_keys={sk} ensure_ascii={ea} separators={sep}", hashlib.sha256(b).hexdigest()))
for nome, h in variants:
    print(f"  {nome:38s} -> {h}  [538f2ca5? {'SIM' if h.startswith('538f2ca5') else 'nao'}]")
print("  Variante(s) a bater no hash predito:", sum(1 for _, h in variants if h.startswith("538f2ca5")))

print()
print("== PASSO 3: ficheiro real GENESIS_STAMP_v4.json (workspace) re-verificado ==")
with open("GENESIS_STAMP_v4.json", "rb") as f:
    raw = f.read()
print("FILE_RAW_BYTES:", len(raw))
print("FILE_RAW_SHA256:", hashlib.sha256(raw).hexdigest())
print("MANIFESTO_DECLARA_3cfe8000...:", hashlib.sha256(raw).hexdigest().startswith("3cfe8000"))
doc = json.loads(raw.decode("utf-8"))
rec = doc["genesis_record"]
print("FILE_RECORD == PASTE_RECORD:", rec == genesis_record)
cb2 = json.dumps(rec, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
print("FILE_CANONICAL_LEN:", len(cb2), "| DECLARADO:", doc["canonical_byte_length"], "| CONFERE:", len(cb2) == doc["canonical_byte_length"])
h2 = hashlib.sha256(cb2).hexdigest()
s2 = hashlib.shake_256(cb2).hexdigest(64)
print("FILE_SHA256_RECALCULADO:", h2)
print("FILE_SHA256_CONFERE_SELO:", h2 == doc["seals"]["sha256"])
print("FILE_SHAKE_RECALCULADO :", s2)
print("FILE_SHAKE_CONFERE_SELO:", s2 == doc["seals"]["shake256_512bit"])
print("TRUE_SHA256 == FILE_SELO:", true_sha256 == doc["seals"]["sha256"])
print("TRUE_SHAKE  == FILE_SELO:", true_shake == doc["seals"]["shake256_512bit"])
