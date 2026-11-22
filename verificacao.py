#!/usr/bin/env python3
# VERIFICAÇÃO BYTE-A-BYTE v2.1.1 (2026-11-22; desde a v2.1 só mudaram comentários) — stdlib-only.
# Igual à v1 nos passos 1 a 3 (mesmo texto de saída) e acrescenta:
#   PASSO 4  — o manifesto e os dois carimbos .ots conferem byte a byte com os hashes fixados;
#   PASSO 4b — lê cada carimbo sem rede: o caminho até ao Bitcoin (bloco, transação, raiz de Merkle) tem de
#              ser o fixado abaixo. Mostra-o por extenso para qualquer pessoa o conferir num explorador público;
#   PASSO 0  — corre antes de tudo: o verificador põe-se à prova a si próprio (autovacina). Dá a si mesmo 3 vetores
#              do NIST, 2 carimbos certos e 5 estragados de propósito; se aceitar um estragado, ler mal um certo ou
#              se o SHA-256 da máquina falhar um vetor do NIST, diz que está estragado e não confere nada;
#   PASSO 5  — veredicto com código de saída: 0 = TUDO CONFERE · 1 = ALGO NÃO CONFERE · 2 = ERRO AO LER ·
#              3 = O VERIFICADOR ESTÁ ESTRAGADO.
# Porquê: quando um ponto não conferia, a v1 escrevia «False» e saía na mesma com 0; e não lia o manifesto
# (relatório do anticorpo de 2026-11-22). Quem só olhava para o código de saída via verde.
# O que não garante: este programa não fala com a rede. Que cada transação está mesmo no bloco indicado
# confere-se num explorador público de Bitcoin ou com `ots verify` (precisa de um nó).
import hashlib
import json
import sys

CLAIMED_PREDICTED = "538f2ca5867a8a3beee6c9c1c19ed63088d7c0b7a6aa3f2385966a35e9d8e530"
# Fixados: os bytes brutos dos dois ficheiros que levam carimbo no Bitcoin (commit 168aea9).
FIXADO_GENESIS_RAW = "3cfe80002b756a40b81ceeae1ff5bec58d55bc49b80303f94cb16164ac036277"
FIXADO_MANIFESTO_RAW = "01721dfa169c8cd8c3ae45f5f6cf454b16efcee963812552b8dbf3e005f80f37"
# Fixados: os bytes brutos dos dois carimbos, já com as quatro atestações Bitcoin (commit 168aea9).
FIXADO_OTS = (
    ("GENESIS_STAMP_v4.json.ots", "c86f83dedd419dfec1d9b2c0ff2e9b77181728b2f212ebe264950dcaa7310592"),
    ("MANIFESTO_HASHES_2026-11-20.txt.ots", "212fee9cbe89c80ca79a9d549fd352acdf754692a6c722c9af128842c2ad8bb3"),
)
MANIFESTO = "MANIFESTO_HASHES_2026-11-20.txt"
OTS_MAGIA = b"\x00OpenTimestamps\x00\x00Proof\x00\xbf\x89\xe2\xe8\x84\xe8\x92\x94"
OTS_TAG_BITCOIN = bytes.fromhex("0588960d73d71901")
# Fixado: o que cada carimbo diz, lido sem rede e conferido a 22-11-2026 contra a biblioteca oficial
# opentimestamps 0.4.5: (hash que carimba, ((bloco, transação, raiz de Merkle, níveis da árvore), ...)).
# Transação e raiz na ordem em que os exploradores as mostram. Que estão mesmo nesses blocos confere-se fora daqui.
_QUATRO = (
    (976735, "1998907025483895bcd4617f98c8ffe316268a6a46233b9f5e8c1b7e15a1d2fc",
     "2fe8d00096f65b0a98749981e02f98fdb5ae4e7ad9e227f919d850d102af25a2", 12),
    (976737, "013201050ba152921e155d704e01f5e2baa6e627c5b58dbf032f3c008ed0607b",
     "4eec22c927674ef26320e4e9794d7231dfa5f7d2cd46819c1df0356f1ce618be", 12),
    (976760, "d508068ca78c8e83e22910b933b5e85b33133674730afd4c310e5ec32a7427d2",
     "43bf508445d58e6e3c4512f1f054f664d568ff5f162d3118abab305e9f5a672f", 12),
    (976761, "43fc515ffb1e7d9de222a3662d489862b3ca7107f6ba9694c5507f316b7b5cb4",
     "7e423ef59adb89318aa547961ccbbd58eb41dff2232be737c980c26d9ae53598", 11),
)
CAMINHOS_FIXADOS = {
    "GENESIS_STAMP_v4.json.ots": (FIXADO_GENESIS_RAW, _QUATRO),
    "MANIFESTO_HASHES_2026-11-20.txt.ots": (FIXADO_MANIFESTO_RAW, _QUATRO),
}

CONFERE = []  # (nome, resultado) — o veredicto final é a soma disto, nada escrito à mão


def conta(nome, ok):
    CONFERE.append((nome, bool(ok)))
    return bool(ok)


def ler(p):
    with open(p, "rb") as f:
        return f.read()


class _Leitor:
    def __init__(self, b):
        self.b, self.i = b, 0

    def bytes_(self, n):
        if self.i + n > len(self.b):
            raise ValueError("o carimbo acaba antes do tempo")
        self.i += n
        return self.b[self.i - n:self.i]

    def varuint(self):
        v, s = 0, 0
        while True:
            c = self.bytes_(1)[0]
            v |= (c & 0x7F) << s
            s += 7
            if not c & 0x80:
                return v

    def varbytes(self):
        return self.bytes_(self.varuint())


def caminhos_ots(dados):
    """Lê um .ots sem rede. Devolve (hash que carimba, [(bloco, txid, raiz de Merkle, níveis)]).
    txid e raiz vêm na ordem em que os exploradores os mostram (bytes invertidos)."""
    L = _Leitor(dados)
    if L.bytes_(len(OTS_MAGIA)) != OTS_MAGIA or L.varuint() != 1 or L.bytes_(1) != b"\x08":
        raise ValueError("cabeçalho do carimbo inesperado")
    carimba = L.bytes_(32)
    achados = []

    def ramo(msg, ops):
        tag = L.bytes_(1)[0]
        while tag == 0xFF:
            passo(L.bytes_(1)[0], msg, ops)
            tag = L.bytes_(1)[0]
        passo(tag, msg, ops)

    def passo(tag, msg, ops):
        if tag == 0x00:
            tipo, carga = L.bytes_(8), _Leitor(L.varbytes())
            if tipo == OTS_TAG_BITCOIN:
                bloco = carga.varuint()
                txid, niveis = None, 0
                for i in range(len(ops) - 1):
                    if ops[i][0] == 0x08 and ops[i + 1][0] == 0x08 and len(ops[i][1]) > 64:
                        txid = ops[i + 1][2]
                        niveis = sum(1 for o in ops[i + 2:] if o[0] in (0xF0, 0xF1))
                        break
                achados.append((bloco, txid[::-1].hex() if txid else None, msg[::-1].hex(), niveis))
            return
        if tag == 0x08:
            novo = hashlib.sha256(msg).digest()
        elif tag == 0xF0:
            novo = msg + L.varbytes()
        elif tag == 0xF1:
            novo = L.varbytes() + msg
        else:
            raise ValueError("operação %02x não prevista" % tag)
        ramo(novo, ops + [(tag, msg, novo)])

    ramo(carimba, [])
    if L.i != len(dados):
        raise ValueError("bytes a mais no fim do carimbo")
    return carimba.hex(), tuple(sorted(achados))


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


# Autovacina: entradas que se sabe estarem certas ou erradas. O carimbo sintético (81 bytes, bloco 12345), a versão
# com o caminho mudado e as 5 estragadas foram conferidos a 22-11-2026 com a biblioteca oficial opentimestamps 0.4.5.
VETORES_NIST = (
    (b"abc", "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"),
    (b"", "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"),
    (b"abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq",
     "248d6a61d20638b8e5c026930c3e6039a33ce45964ff2167f6ecedd419db06c1"),
)
_VAC_CARIMBO = OTS_MAGIA + b"\x01\x08" + bytes(range(32)) + b"\xf0\x01\xaa\x08\x00" + OTS_TAG_BITCOIN + b"\x02\xb9\x60"
_VAC_RAIZ = "f31fb9d6995c2b13794d80fcf7fe01aee35869960568b8c0ca6a9c1f60c10108"
_VAC_RAIZ_MUDADA = "8227d0071d42d742257f0824bf404cd406eaf86242b196e5b49c86b03da95d53"  # com 0xab no lugar de 0xaa


def _ler_vacina(carimbo):
    try:
        return caminhos_ots(carimbo)
    except ValueError:  # a recusa prevista, com motivo
        return "recusado"
    except Exception as e:  # rebentar não é recusar: é um verificador estragado
        return "rebentou (%s)" % type(e).__name__


def autovacina():
    """O verificador contra si próprio. Devolve (provas feitas, o que falhou)."""
    feitas, falhas = 0, []
    for msg, esperado in VETORES_NIST:
        feitas += 1
        if hashlib.sha256(msg).hexdigest() != esperado:
            falhas.append("o SHA-256 desta máquina falha um vetor oficial do NIST")
    certos = (
        ("certo", _VAC_CARIMBO, _VAC_RAIZ),
        ("com o caminho mudado", _VAC_CARIMBO.replace(b"\xf0\x01\xaa", b"\xf0\x01\xab"), _VAC_RAIZ_MUDADA),
    )
    for nome, carimbo, raiz in certos:
        feitas += 1
        if _ler_vacina(carimbo) != (bytes(range(32)).hex(), ((12345, None, raiz, 0),)):
            falhas.append("o leitor de carimbos lê mal um carimbo " + nome)
    estragados = (
        ("cortado no fim", _VAC_CARIMBO[:-1]),
        ("com um byte a mais", _VAC_CARIMBO + b"\x00"),
        ("com a marca do formato trocada", _VAC_CARIMBO[:1] + b"P" + _VAC_CARIMBO[2:]),
        ("com outro tipo de hash do ficheiro", _VAC_CARIMBO[:len(OTS_MAGIA) + 1] + b"\x02" + _VAC_CARIMBO[len(OTS_MAGIA) + 2:]),
        ("com uma operação desconhecida", _VAC_CARIMBO.replace(b"\xf0\x01\xaa", b"\x99\x01\xaa")),
    )
    for nome, carimbo in estragados:
        feitas += 1
        r = _ler_vacina(carimbo)
        if r != "recusado":
            falhas.append("o leitor de carimbos não recusou um carimbo %s: %s" % (nome, "aceitou" if isinstance(r, tuple) else r))
    return feitas, falhas


def principal(vacinas_feitas):
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
    raw = ler("GENESIS_STAMP_v4.json")
    raw_sha = hashlib.sha256(raw).hexdigest()
    print("FILE_RAW_BYTES:", len(raw))
    print("FILE_RAW_SHA256:", raw_sha)
    print("MANIFESTO_DECLARA_3cfe8000...:", conta("bytes brutos = hash fixado", raw_sha == FIXADO_GENESIS_RAW))
    doc = json.loads(raw.decode("utf-8"))
    rec = doc["genesis_record"]
    print("FILE_RECORD == PASTE_RECORD:", conta("registo igual ao do paste", rec == genesis_record))
    cb2 = json.dumps(rec, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    print("FILE_CANONICAL_LEN:", len(cb2), "| DECLARADO:", doc["canonical_byte_length"], "| CONFERE:",
          conta("tamanho canónico declarado", len(cb2) == doc["canonical_byte_length"]))
    h2 = hashlib.sha256(cb2).hexdigest()
    s2 = hashlib.shake_256(cb2).hexdigest(64)
    print("FILE_SHA256_RECALCULADO:", h2)
    print("FILE_SHA256_CONFERE_SELO:", conta("selo sha256 do ficheiro", h2 == doc["seals"]["sha256"]))
    print("FILE_SHAKE_RECALCULADO :", s2)
    print("FILE_SHAKE_CONFERE_SELO:", conta("selo shake256 do ficheiro", s2 == doc["seals"]["shake256_512bit"]))
    print("TRUE_SHA256 == FILE_SELO:", conta("selo sha256 = verdade do paste", true_sha256 == doc["seals"]["sha256"]))
    print("TRUE_SHAKE  == FILE_SELO:", conta("selo shake256 = verdade do paste", true_shake == doc["seals"]["shake256_512bit"]))

    print()
    print("== PASSO 4: manifesto e carimbos .ots ==")
    man = ler(MANIFESTO)
    man_sha = hashlib.sha256(man).hexdigest()
    print("MANIFESTO_RAW_SHA256:", man_sha)
    print("MANIFESTO = hash fixado:", conta("manifesto = hash fixado", man_sha == FIXADO_MANIFESTO_RAW))
    linhas = man.decode("utf-8").splitlines()
    declarado = [l.split()[0] for l in linhas if l.strip().endswith(" GENESIS_STAMP_v4.json") and len(l.split()) == 2]
    print("MANIFESTO declara para o GENESIS:", declarado)
    print("MANIFESTO = bytes do GENESIS:", conta("manifesto declara os bytes do genesis", declarado == [raw_sha]))
    selo_m = [l.split("selo genesis sha256:")[1].split()[0] for l in linhas if "selo genesis sha256:" in l]
    print("MANIFESTO selo genesis = verdade:", conta("manifesto declara o selo verdadeiro", selo_m == [true_sha256]))
    for p, fixado in FIXADO_OTS:
        ots_sha = hashlib.sha256(ler(p)).hexdigest()
        print("OTS", p, "SHA256:", ots_sha)
        print("OTS", p, "= hash fixado:", conta("carimbo " + p + " = hash fixado", ots_sha == fixado))

    print()
    print("== PASSO 4b: o caminho de cada carimbo até ao Bitcoin (lido sem rede) ==")
    for p, ficheiro in (("GENESIS_STAMP_v4.json.ots", raw_sha), (MANIFESTO + ".ots", man_sha)):
        try:
            carimba, achados = caminhos_ots(ler(p))
        except Exception as e:  # carimbo ilegível: o caminho não confere
            carimba, achados = "ilegível (%s: %s)" % (type(e).__name__, e), ()
        print(p, "carimba", carimba)
        for bloco, txid, raiz, niveis in achados:
            print("  bloco %d  transação %s" % (bloco, txid))
            print("              raiz de Merkle %s  (%d níveis)" % (raiz, niveis))
        print(p, "carimba este ficheiro e leva às 4 transações fixadas:",
              conta("caminho de " + p + " = o fixado", carimba == ficheiro and (carimba, achados) == CAMINHOS_FIXADOS[p]))
    print("Para conferir no Bitcoin: procura cada transação num explorador público (tem de estar no")
    print("mesmo bloco, com a mesma raiz de Merkle), ou corre `ots verify` com um nó.")

    print()
    print("== PASSO 0 (corrido antes de tudo): o verificador pôs-se à prova a si próprio ==")
    print("PROVAS FEITAS:", vacinas_feitas, "| FALHAS: 0 (3 vetores do NIST, 2 carimbos certos lidos certos, 5 estragados recusados)")

    print()
    print("== PASSO 5: veredicto ==")
    falhas = [n for n, ok in CONFERE if not ok]
    print("CONFERE %d de %d" % (len(CONFERE) - len(falhas), len(CONFERE)))
    for n in falhas:
        print("  NAO CONFERE:", n)
    print("VEREDICTO:", "TUDO CONFERE" if not falhas else "NAO CONFERE")
    return 0 if not falhas else 1


if __name__ == "__main__":
    try:
        feitas, estragos = autovacina()
        if estragos:
            print("VEREDICTO: O VERIFICADOR ESTÁ ESTRAGADO — não confies em nada do que ele diga:")
            for e in estragos:
                print("  ", e)
            codigo = 3
        else:
            codigo = principal(feitas)
    except Exception as e:  # falta de ficheiro, JSON partido, campo em falta: recusa com motivo, nunca verde
        print("VEREDICTO: ERRO AO LER —", type(e).__name__, e)
        codigo = 2
    sys.exit(codigo)
