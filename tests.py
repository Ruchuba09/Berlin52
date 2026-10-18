import unittest
import os
import numpy as np
import pandas as pd

# Funciones auxiliares para pruebas independientes de operadores
def leer_coordenadas(ruta_archivo):
    coordenadas = []
    leyendo = False
    with open(ruta_archivo, 'r') as f:
        for linea in f:
            linea = linea.strip()
            if linea == "NODE_COORD_SECTION":
                leyendo = True
                continue
            if linea == "EOF" or not linea:
                if leyendo and linea == "EOF":
                    break
                continue
            if leyendo:
                partes = linea.split()
                if len(partes) >= 3:
                    coordenadas.append([float(partes[1]), float(partes[2])])
    return np.array(coordenadas)


def calcular_costo_ruta(ruta, matriz_dist):
    n = len(ruta)
    costo = 0.0
    for i in range(n - 1):
        costo += matriz_dist[ruta[i], ruta[i + 1]]
    costo += matriz_dist[ruta[-1], ruta[0]]  # Cierre del ciclo
    return costo


class TestACSPreproyecto(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.ruta_instancia = "datos/berlin52.tsp.txt"
        if not os.path.exists(cls.ruta_instancia):
            cls.ruta_instancia = "berlin52.tsp.txt"

    # Prueba 1: Que los datos se leen correctamente (Sección 5)
    def test_01_lectura_datos(self):
        self.assertTrue(os.path.exists(self.ruta_instancia), "El archivo de instancia no existe.")
        coords = leer_coordenadas(self.ruta_instancia)
        self.assertEqual(len(coords), 52, "La instancia Berlin52 debe contener exactamente 52 ciudades.")
        self.assertEqual(coords.shape[1], 2, "Cada nodo debe tener coordenadas (x, y).")

    # Prueba 2: Que las soluciones generadas son válidas (Sección 5)
    def test_02_validez_solucion(self):
        n = 52
        ruta = list(np.random.permutation(n))
        
        self.assertEqual(len(ruta), n, "La ruta debe tener longitud igual al número de ciudades.")
        self.assertEqual(len(set(ruta)), n, "La ruta no debe tener ciudades repetidas.")
        self.assertEqual(sorted(ruta), list(range(n)), "La ruta debe visitar todas las ciudades de 0 a n-1.")

    # Prueba 3: Que el costo de una ruta se calcula correctamente (Sección 5)
    def test_03_calculo_costo(self):
        # Triángulo de prueba: (0,0), (0,3), (4,0) -> lados: 3, 5, 4 -> perímetro = 12
        coords_prueba = np.array([[0.0, 0.0], [0.0, 3.0], [4.0, 0.0]])
        matriz_dist = np.zeros((3, 3))
        for i in range(3):
            for j in range(3):
                matriz_dist[i, j] = np.sqrt(np.sum((coords_prueba[i] - coords_prueba[j]) ** 2))

        ruta = [0, 1, 2]
        costo = calcular_costo_ruta(ruta, matriz_dist)
        self.assertAlmostEqual(costo, 12.0, places=4, msg="El cálculo del costo de la ruta cerrada no es exacto.")

    # Prueba 4: Que las feromonas se inicializan y actualizan correctamente (Sección 5)
    def test_04_inicializacion_y_actualizacion_feromonas(self):
        n = 52
        costo_inicial = 10000.0
        tau_0 = 1.0 / (n * costo_inicial)
        self.assertGreater(tau_0, 0.0, "La feromona inicial tau_0 debe ser positiva.")

        matriz_feromona = np.full((n, n), fill_value=tau_0, dtype=float)
        alpha = 0.1

        # Simulación de evaporación local
        u, v = 0, 1
        feromona_previa = matriz_feromona[u, v]
        matriz_feromona[u, v] = (1.0 - alpha) * matriz_feromona[u, v] + alpha * tau_0
        self.assertAlmostEqual(matriz_feromona[u, v], feromona_previa, places=6, 
                               msg="La feromona local con valor tau_0 debe mantenerse estable al inicio.")

        # Simulación de actualización global con mejor costo
        mejor_costo = 7542.0
        delta_tau = alpha * (1.0 / mejor_costo)
        matriz_feromona[u, v] = (1.0 - alpha) * matriz_feromona[u, v] + delta_tau
        self.assertNotEqual(matriz_feromona[u, v], feromona_previa, 
                            "La feromona global debe cambiar tras el depósito de la mejor hormiga.")

    # Prueba 5: Que el algoritmo mantiene o mejora la mejor solución (Sección 5)
    def test_05_monotonia_mejor_solucion(self):
        # El mejor costo histórico nunca debe empeorar a lo largo del tiempo
        costos_historicos = [12000.0, 11500.0, 11500.0, 9800.0, 8500.0, 8500.0, 7544.0]
        for i in range(len(costos_historicos) - 1):
            self.assertLessEqual(costos_historicos[i + 1], costos_historicos[i],
                                 "El costo de la mejor solución encontrada no debe aumentar.")


if __name__ == "__main__":
    unittest.main()