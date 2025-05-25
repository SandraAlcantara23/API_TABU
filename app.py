from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

# Variables globales
estado = {
    "ciudades": [],
    "distancias": {},
    "ruta_actual": [],
    "mejor_ruta": [],
    "distancia_actual": 0,
    "mejor_distancia": float("inf"),
    "memoria_tabu": {},
    "iteracion": 0
}

def calcular_distancia(ruta, distancias):
    total = 0
    for i in range(len(ruta)):
        total += distancias[ruta[i]][ruta[(i + 1) % len(ruta)]]
    return total

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/inicializar", methods=["POST"])
def inicializar():
    datos = request.json
    estado["ciudades"] = datos["ciudades"]
    estado["distancias"] = datos["distancias"]
    estado["ruta_actual"] = random.sample(estado["ciudades"], len(estado["ciudades"]))
    estado["mejor_ruta"] = list(estado["ruta_actual"])
    estado["distancia_actual"] = calcular_distancia(estado["ruta_actual"], estado["distancias"])
    estado["mejor_distancia"] = estado["distancia_actual"]
    estado["memoria_tabu"] = {}
    estado["iteracion"] = 0
    return jsonify({"ruta_inicial": estado["ruta_actual"]})

@app.route("/iterar", methods=["POST"])
def iterar():
    ciudades = estado["ciudades"]
    ruta = estado["ruta_actual"]
    distancias = estado["distancias"]
    mejor_vecino = None
    mejor_distancia = float("inf")

    for i in range(len(ruta)):
        for j in range(i + 1, len(ruta)):
            nueva_ruta = list(ruta)
            nueva_ruta[i], nueva_ruta[j] = nueva_ruta[j], nueva_ruta[i]
            clave = f"{nueva_ruta[i]}_{nueva_ruta[j]}"
            if clave not in estado["memoria_tabu"] and f"{nueva_ruta[j]}_{nueva_ruta[i]}" not in estado["memoria_tabu"]:
                nueva_distancia = calcular_distancia(nueva_ruta, distancias)
                if nueva_distancia < mejor_distancia:
                    mejor_distancia = nueva_distancia
                    mejor_vecino = nueva_ruta

    if mejor_vecino:
        estado["ruta_actual"] = mejor_vecino
        estado["distancia_actual"] = mejor_distancia
        clave_tabu = f"{mejor_vecino[0]}_{mejor_vecino[1]}"
        estado["memoria_tabu"][clave_tabu] = 5
        if mejor_distancia < estado["mejor_distancia"]:
            estado["mejor_ruta"] = list(mejor_vecino)
            estado["mejor_distancia"] = mejor_distancia

    estado["iteracion"] += 1
    nuevas_claves = {}
    for k in list(estado["memoria_tabu"].keys()):
        if estado["memoria_tabu"][k] > 1:
            nuevas_claves[k] = estado["memoria_tabu"][k] - 1
    estado["memoria_tabu"] = nuevas_claves

    return jsonify({
        "ruta_actual": estado["ruta_actual"],
        "distancia_actual": estado["distancia_actual"],
        "mejor_ruta": estado["mejor_ruta"],
        "mejor_distancia": estado["mejor_distancia"],
        "iteracion": estado["iteracion"]
    })

@app.route("/estado")
def obtener_estado():
    return jsonify({
        "ruta_actual": estado["ruta_actual"],
        "distancia_actual": estado["distancia_actual"],
        "mejor_ruta": estado["mejor_ruta"],
        "mejor_distancia": estado["mejor_distancia"],
        "iteracion": estado["iteracion"]
    })

if __name__ == "__main__":
    app.run(debug=True)
