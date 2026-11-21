#!/usr/bin/env python3
# SPDX-License-Identifier: EUPL-1.2
# KCP/0.1 — verificador de referência. Corre fora de qualquer IA. Só biblioteca-padrão + konfirmu_calc.py ao lado.
# Uso: python3 kcp_verificar.py pacote.json [PUB_ACEITE ...]
#   pacote.json = {"claim": {...}, "selo": {...}}  (ou {"resposta": {...}, "selo_konfirmu": {...}} da API Konfirmu)
import json, os, sys, unicodedata
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import konfirmu_calc as K  # v2.5.1 (referência) ou v2.8


def nfc(o):
    if isinstance(o, str):
        return unicodedata.normalize("NFC", o)
    if isinstance(o, dict):
        return {nfc(k): nfc(v) for k, v in o.items()}
    if isinstance(o, list):
        return [nfc(v) for v in o]
    return o


def verificar(pacote, aceites=None):
    claim = pacote.get("claim", pacote.get("resposta"))
    selo = pacote.get("selo", pacote.get("selo_konfirmu"))
    if not isinstance(claim, dict) or not isinstance(selo, dict) or not claim.get("o_que_nao_garante"):
        return "NAO_VERIFICADO", "falta o CLAIM, o selo ou o o_que_nao_garante"
    ok = K.selo_ok(nfc(claim), selo, aceites=aceites or None)
    return ("VERIFICADO" if ok else "NAO_VERIFICADO"), ("selo confere" if ok else "o selo não confere com este CLAIM e esta chave")


if __name__ == "__main__":
    estado, porque = verificar(json.load(open(sys.argv[1], encoding="utf-8")), sys.argv[2:])
    print(estado, "—", porque)
    sys.exit(0 if estado == "VERIFICADO" else 1)
