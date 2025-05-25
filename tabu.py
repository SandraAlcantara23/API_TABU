import random

class BusquedaTabuTSP:
    def __init__(self, ruta_inicial, distancias, duracion_tabu=5):
        self.estado_actual = ruta_inicial[:]
        self.mejor_estado = ruta_inicial[:]
        self.distancias = distancias
        self.memoria_tabu = {}
        self.duracion_tabu = duracion_tabu
        self.iteracion = 0

    def evaluar(self, ruta):
        total = 0
        for i in range(len(ruta) - 1):
            total += self.distancias[ruta[i]][ruta[i+1]]
        total += self.distancias[ruta[-1]][ruta[0]]
        return total

    def generar_vecinos(self):
        vecinos = []
        for i in range(len(self.estado_actual)):
            for j in range(i + 1, len(self.estado_actual)):
                vecino = self.estado_actual[:]
                vecino[i], vecino[j] = vecino[j], vecino[i]
                vecinos.append((vecino, (self.estado_actual[i], self.estado_actual[j])))
        return vecinos

    def es_tabu(self, c1, c2):
        return f"{c1}_{c2}" in self.memoria_tabu or f"{c2}_{c1}" in self.memoria_tabu

    def iterar(self):
        vecinos = self.generar_vecinos()
        mejor_vecino = None
        mejor_valor = float('inf')
        cambio_realizado = None

        for vecino, cambio in vecinos:
            if not self.es_tabu(cambio[0], cambio[1]):
                valor = self.evaluar(vecino)
                if valor < mejor_valor:
                    mejor_valor = valor
                    mejor_vecino = vecino
                    cambio_realizado = cambio

        if mejor_vecino:
            self.estado_actual = mejor_vecino
            clave = f"{cambio_realizado[0]}_{cambio_realizado[1]}"
            self.memoria_tabu[clave] = self.duracion_tabu
            if mejor_valor < self.evaluar(self.mejor_estado):
                self.mejor_estado = mejor_vecino

        # Actualizar memoria tabú
        claves_a_eliminar = []
        for clave in self.memoria_tabu:
            self.memoria_tabu[clave] -= 1
            if self.memoria_tabu[clave] <= 0:
                claves_a_eliminar.append(clave)
        for clave in claves_a_eliminar:
            del self.memoria_tabu[clave]

        self.iteracion += 1

    def estado(self):
        return {
            'iteracion': self.iteracion,
            'ruta_actual': self.estado_actual,
            'distancia_actual': self.evaluar(self.estado_actual),
            'mejor_ruta': self.mejor_estado,
            'mejor_distancia': self.evaluar(self.mejor_estado)
        }
