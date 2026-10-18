import numpy as np
import pandas as pd
import random


def leer_coordenadas(ruta_archivo):
    """Lee el archivo TSPLIB y retorna matriz numpy de coordenadas (x, y)."""
    coordenadas = pd.read_table(ruta_archivo, header=None, sep=r'\s+', skiprows=6, skipfooter=2, engine='python')
    return coordenadas.drop(columns=0).to_numpy()


def calcular_matriz_distancias(coords):
    """Genera la matriz simétrica de distancias euclidianas D_ij."""
    n = len(coords)
    matriz = np.zeros((n, n), dtype=float)
    for i in range(n - 1):
        for j in range(i + 1, n):
            d = np.sqrt(np.sum((coords[i] - coords[j]) ** 2))
            matriz[i, j] = d
            matriz[j, i] = d
    return matriz


def calcular_matriz_heuristica(matriz_dist):
    """Calcula la visibilidad eta_ij = 1 / d_ij con ceros en la diagonal."""
    with np.errstate(divide='ignore'):
        eta = np.full_like(matriz_dist, fill_value=1.0 / matriz_dist, dtype=float)
    np.fill_diagonal(eta, 0.0)
    return eta


def calcular_costo_ruta(n, ruta, matriz_dist):
    """Calcula la distancia acumulada del ciclo cerrado TSP."""
    costo = matriz_dist[ruta[n - 1], ruta[0]]
    for i in range(n - 1):
        costo += matriz_dist[ruta[i], ruta[i + 1]]
    return costo


def seleccionar_siguiente_nodo(nodo_actual, memoria_k, matriz_tau, matriz_eta, beta, q0, n):
    """Aplica la regla de transición pseudo-aleatoria proporcional (q0)."""
    Tall = memoria_k * matriz_tau[nodo_actual, :] * np.power(matriz_eta[nodo_actual, :], beta)
    
    if np.random.rand() < q0:
        return np.random.choice(np.where(Tall == Tall.max())[0])
    else:
        suma_tall = Tall.sum()
        if suma_tall > 0:
            ruleta = Tall / suma_tall
            ruleta_acumulada = np.cumsum(ruleta)
            rTiro = np.random.rand()
            return np.where(ruleta_acumulada >= rTiro)[0][0]
        else:
            no_visitados = np.where(memoria_k == 1)[0]
            return np.random.choice(no_visitados)


def evaporacion_local(matriz_tau, u, v, alpha, tau_0):
    """Aplica la regla de evaporación local de feromonas sobre el arco (u, v)."""
    nueva = ((1.0 - alpha) * matriz_tau[u, v]) + (alpha * tau_0)
    matriz_tau[u, v] = nueva
    matriz_tau[v, u] = nueva


def evaporacion_global(matriz_tau, mejor_ruta, mejor_costo, alpha, n):
    """Aplica evaporación general y refuerzo exclusivo sobre la mejor ruta global."""
    matriz_tau *= (1.0 - alpha)
    delta_tau = alpha * (1.0 / mejor_costo)
    for i in range(n - 1):
        u, v = mejor_ruta[i], mejor_ruta[i + 1]
        matriz_tau[u, v] += delta_tau
        matriz_tau[v, u] = matriz_tau[u, v]
    u, v = mejor_ruta[-1], mejor_ruta[0]
    matriz_tau[u, v] += delta_tau
    matriz_tau[v, u] = matriz_tau[u, v]