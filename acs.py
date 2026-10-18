import sys
import time
import os
import csv
import numpy as np
import pandas as pd


def solucionCalculoCosto(n, s, c):
    """Calcula la distancia total recorrida en el ciclo cerrado del TSP."""
    aux = c[s[n - 1], s[0]]
    for i in range(n - 1):
        aux += c[s[i], s[i + 1]]
    return aux


def main():
    # 1. Captura de parámetros por línea de comandos (orden exacto del enunciado)
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
        # Valores por defecto para pruebas rápidas
        entrada = 'datos/berlin52.tsp.txt'
        tamColonia = 50
        ite = 200
        tev = 0.1
        beta = 2.5
        q0 = 0.9
        semilla = 12345
        archivo_salida = 'resultados/resultados.csv'

    col = tamColonia
    tiempo_proceso_ini = time.process_time()
    np.random.seed(semilla)

    print(f"Ejecutando ACS sobre: {entrada}")
    print(f"Parámetros: Hormigas={tamColonia}, Iteraciones={ite}, Alpha={tev}, Beta={beta}, q0={q0}, Semilla={semilla}")

    # 2. Lectura del archivo de coordenadas TSPLIB
    try:
        matrizCoordenadas = pd.read_table(entrada, header=None, sep=r'\s+', skiprows=6, skipfooter=2, engine='python')
        matrizCoordenadas = matrizCoordenadas.drop(columns=0).to_numpy()
    except Exception as e:
        print(f"Error al leer el archivo {entrada}: {e}")
        sys.exit(1)

    numVariables = matrizCoordenadas.shape[0]

    # 3. Generación de la matriz de distancias euclidianas (D_ij)
    matrizDistancias = np.full((numVariables, numVariables), fill_value=-1.0, dtype=float)
    for i in range(numVariables - 1):
        for j in range(i + 1, numVariables):
            matrizDistancias[i, j] = np.sqrt(np.sum(np.square(matrizCoordenadas[i] - matrizCoordenadas[j])))
            matrizDistancias[j, i] = matrizDistancias[i, j]

    # 4. Generación de la matriz de información heurística (eta_ij = 1 / d_ij)
    with np.errstate(divide='ignore'):
        matrizHeuristica = np.full_like(matrizDistancias, fill_value=1.0 / matrizDistancias, dtype=float)
    np.fill_diagonal(matrizHeuristica, 0.0)

    # 5. Generación de una solución inicial aleatoria para fijar tau_0
    solucionMejor = np.arange(0, numVariables)
    np.random.shuffle(solucionMejor)
    solucionMejorCosto = solucionCalculoCosto(numVariables, solucionMejor, matrizDistancias)
    solucionMejorIteracion = 0

    # 6. Inicialización de la matriz de feromonas
    tij0 = 1.0 / (numVariables * solucionMejorCosto)
    matrizFeromonas = np.full((numVariables, numVariables), fill_value=tij0, dtype=float)

    generacion = 0

    # 7. Ciclo principal del algoritmo ACS
    while generacion < ite:
        generacion += 1

        colonia = np.full((tamColonia, numVariables), fill_value=-1, dtype=int)
        memoria = np.ones((col, numVariables), dtype=int)

        # Asignar nodo inicial aleatorio a cada hormiga
        for k in range(col):
            colonia[k, 0] = np.random.randint(numVariables)
            memoria[k][colonia[k, 0]] = 0

        # Construcción paso a paso de las rutas
        for i in range(numVariables - 1):
            for k in range(col):
                nodo_actual = colonia[k, i]
                Tall = memoria[k] * matrizFeromonas[nodo_actual, :] * np.power(matrizHeuristica[nodo_actual, :], beta)

                # Regla de transición pseudo-aleatoria proporcional (q0)
                if np.random.rand() < q0:
                    j0 = np.random.choice(np.where(Tall == Tall.max())[0])
                    colonia[k, i + 1] = j0
                    memoria[k][j0] = 0
                else:
                    suma_tall = Tall.sum()
                    if suma_tall > 0:
                        ruleta = Tall / suma_tall
                        ruleta_acumulada = np.cumsum(ruleta)
                        rTiro = np.random.rand()
                        j0 = np.where(ruleta_acumulada >= rTiro)[0][0]
                    else:
                        no_visitados = np.where(memoria[k] == 1)[0]
                        j0 = np.random.choice(no_visitados)

                    colonia[k, i + 1] = j0
                    memoria[k][j0] = 0

                # Evaporación local de feromona
                siguiente = colonia[k, i + 1]
                nueva_feromona = ((1.0 - tev) * matrizFeromonas[nodo_actual, siguiente]) + (tev * tij0)
                matrizFeromonas[nodo_actual, siguiente] = nueva_feromona
                matrizFeromonas[siguiente, nodo_actual] = nueva_feromona

        # Cierre del ciclo y evaporación local de la última arista
        for k in range(col):
            u, v = colonia[k, -1], colonia[k, 0]
            nueva_feromona = ((1.0 - tev) * matrizFeromonas[u, v]) + (tev * tij0)
            matrizFeromonas[u, v] = nueva_feromona
            matrizFeromonas[v, u] = nueva_feromona

        # Evaluación de las soluciones de la iteración
        for k in range(col):
            solucionCosto = solucionCalculoCosto(numVariables, colonia[k], matrizDistancias)
            if solucionCosto < solucionMejorCosto:
                solucionMejorCosto = solucionCosto
                solucionMejor = colonia[k].copy()
                solucionMejorIteracion = generacion

        # Actualización global de feromonas (solo deposita la mejor hormiga)
        matrizFeromonas = (1.0 - tev) * matrizFeromonas
        delta_tau = tev * (1.0 / solucionMejorCosto)
        for i in range(numVariables - 1):
            u, v = solucionMejor[i], solucionMejor[i + 1]
            matrizFeromonas[u, v] += delta_tau
            matrizFeromonas[v, u] = matrizFeromonas[u, v]
        u, v = solucionMejor[-1], solucionMejor[0]
        matrizFeromonas[u, v] += delta_tau
        matrizFeromonas[v, u] = matrizFeromonas[u, v]

    tiempo_cpu = time.process_time() - tiempo_proceso_ini

    print(f"\nEjecución finalizada con éxito.")
    print(f"Mejor distancia obtenida: {solucionMejorCosto:.4f}")
    print(f"Encontrada en la iteración: {solucionMejorIteracion}")
    print(f"Tiempo de CPU: {tiempo_cpu:.4f} s")

    # 8. Guardar salida en archivo CSV estructurado
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

    print(f"Resultados registrados en: {archivo_salida}")


if __name__ == "__main__":
    main()