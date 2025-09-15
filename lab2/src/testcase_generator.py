import json
import random
import os

def gerar_caso_realista_intercalado(total_voos, num_urgencias, num_liberadas):
    folder_saida = f"{total_voos}_voos"
    os.makedirs(folder_saida, exist_ok=True)

    voos = list(range(1001, 1001 + total_voos))
    cidades = [f"Cidade{i}" for i in range(1, total_voos + 1)]

    chegada = list(zip(voos, cidades))
    random.shuffle(chegada)

    urgencias = set(random.sample(voos, min(num_urgencias, total_voos)))

    liberadas_posicoes = sorted(random.sample(range(total_voos + num_liberadas // 2), min(num_liberadas, total_voos)))

    entrada = [
        "Joseloid International Airport",
        "Torre de controle: mensagens recebidas",
        "=========================================",
        "MESSAGE           FLIGHT  FROM\n",
        "INICIO              0000  -"
    ]

    autorizados = []
    fila_voos = []

    i_chegada = 0
    for i in range(total_voos + len(liberadas_posicoes) // 2):
        if i in liberadas_posicoes:
            entrada.append("pista_liberada      0000  -")
            if fila_voos:
                idx = next((j for j, (v, c, u) in enumerate(fila_voos) if u), 0)
                voo, cidade, _ = fila_voos.pop(idx)
                autorizados.append(str(voo))
            else:
                autorizados.append("0000")
        elif i_chegada < total_voos:
            voo, cidade = chegada[i_chegada]
            i_chegada += 1
            urg = 1 if voo in urgencias else 0
            fila_voos.append((voo, cidade, urg))
            entrada.append(f"pede_pouso          {voo}  {cidade}")
            if urg == 1:
                entrada.append(f"URGENCIA            {voo} -")

    entrada.append("FIM                 0000  -")

    pendentes = [str(v) for v, c, u in fila_voos]

    flight_origins = {str(v): c for v, c, u in fila_voos if v != 0}

    for voo in autorizados:
        if voo != "0000":
            v = int(voo)
            cidade = next((c for vv, c in chegada if vv == v), None)
            if cidade:
                flight_origins[voo] = cidade

    nome_entrada = os.path.join(folder_saida, "entrada2.txt")
    nome_saida = os.path.join(folder_saida, "saida2.json")

    with open(nome_entrada, "w") as f:
        f.write("\n".join(entrada))
    with open(nome_saida, "w") as f:
        json.dump({
            "ordem_voos": {"authorized": autorizados, "pending": pendentes},
            "flight_origins": flight_origins
        }, f, indent=2)

casos = [
    (30, 5, 20),
    (50, 10, 35),
    (100, 20, 70),
    (200, 40, 140),
    (500, 100, 350)
]

for total, urg, lib in casos:
    gerar_caso_realista_intercalado(total, urg, lib)
