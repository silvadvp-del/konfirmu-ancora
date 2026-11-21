# KCP/0.2 — medições com a calculadora de referência (não altera a calculadora)
import sys, time, json, itertools, hashlib, platform
sys.path.insert(0, sys.argv[1])
import konfirmu_calc as K
out = {"calc_versao": K.VERSAO, "python": platform.python_version(), "maquina": platform.machine()}
sk = hashlib.sha256(b"kcp02/chave-de-teste-publica").digest()
claim = {"kcp": "0.2", "emissor": "teste", "emitido_em": "2026-11-21T00:00:00Z", "veredicto": "VERIFICADO",
         "o_que_nao_garante": "vetor de teste", "footprint": {"gco2e": 0.0, "water_ml": 0.0, "method": "teste", "basis": "estimated"}}
selo = K.selar(claim, sk)
N = 20
pares = [(dict(claim, n=i), None) for i in range(N)]
pares = [(c, K.selar(c, sk)) for c, _ in pares]  # N CLAIMs diferentes: sem cache a ajudar
t0 = time.process_time(); ok = all(K.selo_ok(c, s) for c, s in pares); cpu = (time.process_time() - t0) / N
mau = dict(claim, veredicto="DIVERGE_DA_FICHA")
out["verify"] = {"n": N, "todos_ok": ok, "adulterado_recusado": not K.selo_ok(mau, selo), "cpu_s_por_verify": round(cpu, 6), "sla_1s": cpu < 1.0}
# pegada: E = P·t ; gCO2e = E·intensidade  (P e intensidade ASSUMIDOS, declarados)
P_W, I_g_kWh = 10.0, 400.0
E_J = P_W * cpu; g = E_J / 3.6e6 * I_g_kWh
out["pegada_verify_local"] = {"assumido": {"potencia_W": P_W, "intensidade_gCO2e_por_kWh": I_g_kWh}, "energia_J": round(E_J, 6),
                              "gco2e": float("%.3g" % g), "alvo_da_ordem_gco2e": 1.7, "razao_alvo_sobre_medido": float("%.3g" % (1.7 / g))}
# Shamir 4-de-6 com os nomes das câmaras
cam = ["AFRICA", "EUROPE", "ASIA", "AMERICAS", "CIVIL_SOCIETY", "SCIENCE"]
seg = int.from_bytes(sk, "big")
partes = K.shamir_partir(seg, 4, 6, b"kcp02/semente-declarada")
q4 = all(K.shamir_juntar(list(t)) == seg for t in itertools.combinations(partes, 4))
q3 = all(K.shamir_juntar(list(t)) != seg for t in itertools.combinations(partes, 3))
out["shamir_4_de_6"] = {"camaras": cam, "quartetos_reconstroem": q4, "n_quartetos": 15, "trios_nao_reconstroem": q3, "n_trios": 20}
out["p6_tem_RECONCILIADO"] = "RECONCILIADO" in open(K.__file__, encoding="utf-8").read()
print(json.dumps(out, ensure_ascii=False, indent=1))
