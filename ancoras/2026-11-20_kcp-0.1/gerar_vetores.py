#!/usr/bin/env python3
# Gera os vetores de teste do KCP/0.1 com a implementação de referência (v2.5.1) e confere-os com a v2.8.
import hashlib, importlib.util, json, sys
def carregar(nome, caminho):
    s = importlib.util.spec_from_file_location(nome, caminho); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
R = carregar("v251", "/home/claude/k251/konfirmu_calc.py")
N = carregar("v28", "/home/claude/k28/konfirmu_calc.py")
assert hashlib.sha256(open("/home/claude/k251/konfirmu_calc.py","rb").read()).hexdigest().startswith("7b0680f7")
SK = hashlib.sha256("KCP/0.1 vetor de teste — chave PÚBLICA, nunca usar".encode()).digest()
ficha = {"id": "KF-DEMO-001", "facto": "A Bíblia de Gutenberg teve uma tiragem de cerca de 180 exemplares.",
         "fonte": "https://www.loc.gov/exhibits/bibles/interactives/gutenberg/index.html", "data": "2026-11-20",
         "nao_garante": "o número exato não é conhecido; as estimativas vão de 158 a 180"}
claim = {"kcp": "0.1", "emissor": "konfirmu/v1/verificar", "emitido_em": "2026-11-20T12:00:00Z",
         "afirmacao_sha256": R.h256("A Bíblia de Gutenberg teve uma tiragem de cerca de 180 exemplares.".encode()),
         "veredicto": "VERIFICADO", "facto_selado": dict(ficha, hash=R.hobj(ficha)),
         "o_que_nao_garante": "VERIFICADO quer dizer que a afirmação bate com uma ficha com fonte, não que a fonte é infalível.",
         "numero_exemplo": 0.1 + 0.2}
C = R.canon(claim)
selo = R.selar(claim, SK)
assert R.hobj(ficha) == N.hash_da_ficha(ficha)
assert C == N.canon(claim) and selo == N.selar(claim, SK), "v2.5.1 e v2.8 divergem"
assert R.selo_ok(claim, selo) and N.selo_ok(claim, selo, aceites=[selo["pub"]])
mau = dict(claim, veredicto="SEM_COBERTURA")
assert not R.selo_ok(mau, selo) and not N.selo_ok(mau, selo)
v = {"chave_de_teste_sk_hex": SK.hex(), "aviso": "chave PÚBLICA de teste: nunca usar em produção",
     "claim": claim, "canonico_utf8": C.decode("utf-8"), "canonico_sha256": hashlib.sha256(C).hexdigest(),
     "canonico_bytes": len(C), "selo": selo,
     "negativo": {"mudanca": "veredicto VERIFICADO -> SEM_COBERTURA", "esperado": "NAO_VERIFICADO"},
     "conferido_com": {"v2.5.1": "7b0680f795d9614bf6de97dae507db3b21d61f99742753ef444565d0b32086a6",
                       "v2.8": hashlib.sha256(open("/home/claude/k28/konfirmu_calc.py","rb").read()).hexdigest()}}
json.dump(v, open("kcp_vetores_0.1.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(C.decode()); print(json.dumps(selo, indent=1)); print("v2.5.1 == v2.8; negativo recusado")
