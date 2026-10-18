import sys
import os
import pandas as pd
import numpy as np
import igraph as ig


def leer_coordenadas_tsp(ruta_archivo):
    """Extrae las coordenadas (x, y) de las ciudades desde el archivo TSPLIB."""
    coordenadas = []
    leyendo_nodos = False
    with open(ruta_archivo, 'r') as f:
        for linea in f:
            linea = linea.strip()
            if linea == "NODE_COORD_SECTION":
                leyendo_nodos = True
                continue
            if linea == "EOF" or not linea:
                if leyendo_nodos and linea == "EOF":
                    break
                continue
            if leyendo_nodos:
                partes = linea.split()
                if len(partes) >= 3:
                    coordenadas.append([float(partes[1]), float(partes[2])])
    return np.array(coordenadas)


def construir_grafo(tam, sol, coordenadas):
    """Construye la estructura de grafo y layout para renderizado con igraph."""
    etiqueta = [str(x) for x in range(tam)]
    aristas = []
    for i in range(tam - 1):
        aristas.append([sol[i], sol[i + 1]])
    aristas.append([sol[-1], sol[0]])

    color = ['red'] * tam
    color[aristas[0][0]] = 'blue'

    g = ig.Graph(n=tam, directed=True)
    g.add_edges(aristas)
    g.vs["label"] = etiqueta
    g.vs["color"] = color
    g.vs["label_size"] = 7
    g.vs["size"] = 14
    g.es["edge_size"] = 1.5

    layout = ig.Layout(coords=coordenadas.tolist())
    return g, layout


def main():
    archivo_csv = sys.argv[1] if len(sys.argv) > 1 else "resultados/resultados.csv"
    carpeta_graficos = "graficos"
    os.makedirs(carpeta_graficos, exist_ok=True)

    if not os.path.exists(archivo_csv):
        print(f"Error: No se encontró el archivo '{archivo_csv}'.")
        sys.exit(1)

    df = pd.read_csv(archivo_csv)
    if df.empty or 'Ruta' not in df.columns:
        print("Error: El archivo CSV no contiene registros válidos o falta la columna 'Ruta'.")
        sys.exit(1)

    print(f"Procesando {len(df)} corridas registradas en {archivo_csv}...\n")

    for i, fila in df.iterrows():
        ruta = [int(nodo) for nodo in str(fila['Ruta']).split('-')]
        costo = float(fila['Mejor_Costo'])
        semilla = fila['Semilla']
        hormigas = fila['Hormigas']
        archivo_instancia = fila['Instancia']

        if not os.path.exists(archivo_instancia):
            archivo_instancia = "datos/berlin52.tsp.txt"

        coordenadas = leer_coordenadas_tsp(archivo_instancia)
        grafo, layout = construir_grafo(len(ruta), ruta, coordenadas)

        # Guarda exclusivamente la imagen identificada por experimento
        nombre_archivo = f"grafico_exp{i+1:02d}_s{semilla}_h{hormigas}_c{int(costo)}.png"
        ruta_salida = os.path.join(carpeta_graficos, nombre_archivo)

        ig.plot(
            grafo,
            target=ruta_salida,
            layout=layout,
            bbox=(800, 600),
            margin=40,
            background="white"
        )
        print(f"[{i+1}/{len(df)}] Guardado: {ruta_salida} (Costo: {costo:.2f})")

    print(f"\nProceso finalizado. Todas las imágenes están en la carpeta '{carpeta_graficos}/'.")


if __name__ == "__main__":
    main()