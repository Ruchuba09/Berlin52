import sys
import time
import os
import csv
import numpy as np
import operadores as op


def main():
    if len(sys.argv) >= 9:
        entrada = sys.argv[1]
        tamColonia = int(sys.argv[2])
        ite = int(sys.argv[3])
        tev = float(sys.argv[4])
        beta = float(sys.argv[5])
        q0 = float(sys.argv[6])
        semilla = int(sys.argv[7])
        archivo_salida = sys.argv[8]
    else:
        entrada = 'datos/berlin52.tsp.txt'
        tamColonia, ite, tev, beta, q0, semilla = 50, 200, 0.1, 2.5, 0.9, 12345
        archivo_salida = 'resultados/resultados.csv'

    tiempo_proceso_ini = time.process_time()
    np.random.seed(semilla)

    # 1. Inicialización mediante operadores
    coords = op.leer_coordenadas(entrada)
    numVariables = coords.shape[0]
    matrizDistancias = op.calcular_matriz_distancias(coords)
    matrizHeuristica = op.calcular_matriz_heuristica(matrizDistancias)

    solucionMejor = np.arange(0, numVariables)
    np.random.shuffle(solucionMejor)
    solucionMejorCosto = op.calcular_costo_ruta(numVariables, solucionMejor, matrizDistancias)
    solucionMejorIteracion = 0

    tij0 = 1.0 / (numVariables * solucionMejorCosto)
    matrizFeromonas = np.full((numVariables, numVariables), fill_value=tij0, dtype=float)

    # 2. Ciclo principal ACS
    for generacion in range(1, ite + 1):
        colonia = np.full((tamColonia, numVariables), fill_value=-1, dtype=int)
        memoria = np.ones((tamColonia, numVariables), dtype=int)

        for k in range(tamColonia):
            colonia[k, 0] = np.random.randint(numVariables)
            memoria[k][colonia[k, 0]] = 0

        # Construcción y evaporación local
        for i in range(numVariables - 1):
            for k in range(tamColonia):
                actual = colonia[k, i]
                sig = op.seleccionar_siguiente_nodo(
                    actual, memoria[k], matrizFeromonas, matrizHeuristica, beta, q0, numVariables
                )
                colonia[k, i + 1] = sig
                memoria[k][sig] = 0
                op.evaporacion_local(matrizFeromonas, actual, sig, tev, tij0)

        # Cierre del tour
        for k in range(tamColonia):
            op.evaporacion_local(matrizFeromonas, colonia[k, -1], colonia[k, 0], tev, tij0)

        # Evaluación de la iteración
        for k in range(tamColonia):
            costo = op.calcular_costo_ruta(numVariables, colonia[k], matrizDistancias)
            if costo < solucionMejorCosto:
                solucionMejorCosto = costo
                solucionMejor = colonia[k].copy()
                solucionMejorIteracion = generacion

        # Actualización global de feromona
        op.evaporacion_global(matrizFeromonas, solucionMejor, solucionMejorCosto, tev, numVariables)

    tiempo_cpu = time.process_time() - tiempo_proceso_ini

    # 3. Guardado estructurado
    directorio_salida = os.path.dirname(archivo_salida)
    if directorio_salida:
        os.makedirs(directorio_salida, exist_ok=True)

    archivo_existe = os.path.isfile(archivo_salida)
    with open(archivo_salida, mode='a', newline='') as f:
        writer = csv.writer(f)
        if not archivo_existe:
            writer.writerow(['Instancia', 'Semilla', 'Hormigas', 'Iteraciones', 'Evaporacion', 'Beta', 'q0', 'Mejor_Costo', 'Iteracion_Mejor', 'Tiempo_CPU', 'Ruta'])
        writer.writerow([
            entrada, semilla, tamColonia, ite, tev, beta, q0,
            round(solucionMejorCosto, 4), solucionMejorIteracion,
            round(tiempo_cpu, 4), "-".join(map(str, solucionMejor))
        ])


if __name__ == "__main__":
    main()