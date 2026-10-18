# Berlin52 - Sistema de Colonia de Hormigas (ACS) en TSP

Implementación modular de la metaheurística Sistema de Colonia de Hormigas (*Ant Colony System*, ACS) aplicada al Problema del Vendedor Viajero (TSP) sobre la instancia estándar Berlin52.

---

## 1. Requisitos e Instalación

Para ejecutar este proyecto se requiere Python 3.8 o superior e instalar el conjunto completo de dependencias mediante el archivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

---

## 2. Estructura del Proyecto

El repositorio sigue una organización modular con separación de responsabilidades:

```text
Berlin52/
├── acs.py                 # Orquestador del flujo principal del algoritmo ACS
├── operadores.py          # Biblioteca de funciones matemáticas y operadores
├── tests.py               # Casos de prueba unitarios automatizados
├── graficar.py            # Generación de gráficos a partir de resultados.csv
├── requirements.txt       # Dependencias del proyecto
├── datos/
│   └── berlin52.tsp.txt   # Instancia con coordenadas cartesianas de 52 ciudades
├── resultados/
│   └── resultados.csv     # Archivo estructurado con los resultados experimentales
├── graficos/              # Gráficos generados para cada experimento
│   ├── grafico_exp01_s12345_h50_c7544.png
│   └── ...
└── README.md              # Documentación técnica y guía de uso
```

---

## 3. Guía de Ejecución

### A. Ejecución del Algoritmo Principal (`acs.py`)
El programa se ejecuta por línea de comandos especificando los parámetros en el orden requerido:

```bash
python acs.py <instancia> <n_hormigas> <iteraciones> <alpha> <beta> <q0> <semilla> <archivo_salida>
```

* `<instancia>`: Ruta al archivo de coordenadas (ej. `datos/berlin52.tsp.txt`).
* `<n_hormigas>`: Cantidad de hormigas en la colonia (ej. `50`).
* `<iteraciones>`: Número de iteraciones del ciclo principal (ej. `200`).
* `<alpha>`: Tasa de evaporación de feromonas (ej. `0.1`).
* `<beta>`: Peso de la información heurística (ej. `2.5`).
* `<q0>`: Probabilidad límite de explotación pseudo-aleatoria (ej. `0.9`).
* `<semilla>`: Valor entero para el control de reproducibilidad (ej. `12345`).
* `<archivo_salida>`: Ruta del archivo CSV donde se registrarán los resultados (ej. `resultados/resultados.csv`).

**Ejemplo de ejecución estándar:**
```bash
python acs.py datos/berlin52.tsp.txt 50 200 0.1 2.5 0.9 12345 resultados/resultados.csv
```

---

### B. Batería de Pruebas Experimentales
Para registrar el conjunto de experimentos y evaluar el impacto de cada parámetro:

```bash
# 1. Variabilidad por semilla
python acs.py datos/berlin52.tsp.txt 50 200 0.1 2.5 0.9 12345 resultados/resultados.csv
python acs.py datos/berlin52.tsp.txt 50 200 0.1 2.5 0.9 23456 resultados/resultados.csv
python acs.py datos/berlin52.tsp.txt 50 200 0.1 2.5 0.9 34567 resultados/resultados.csv
python acs.py datos/berlin52.tsp.txt 50 200 0.1 2.5 0.9 45678 resultados/resultados.csv

# 2. Variación de tamaño de colonia (hormigas)
python acs.py datos/berlin52.tsp.txt 10 200 0.1 2.5 0.9 12345 resultados/resultados.csv
python acs.py datos/berlin52.tsp.txt 30 200 0.1 2.5 0.9 12345 resultados/resultados.csv
python acs.py datos/berlin52.tsp.txt 80 200 0.1 2.5 0.9 12345 resultados/resultados.csv

# 3. Variación del número de iteraciones
python acs.py datos/berlin52.tsp.txt 50 50 0.1 2.5 0.9 12345 resultados/resultados.csv
python acs.py datos/berlin52.tsp.txt 50 400 0.1 2.5 0.9 12345 resultados/resultados.csv

# 4. Variación de parámetros propios de ACS (q0 y beta)
python acs.py datos/berlin52.tsp.txt 50 200 0.1 2.5 0.5 12345 resultados/resultados.csv
python acs.py datos/berlin52.tsp.txt 50 200 0.1 5.0 0.9 12345 resultados/resultados.csv
```

---

### C. Ejecución de Pruebas Unitarias (`tests.py`)
Para verificar la lectura de archivos, el cálculo exacto de distancias, la validez de las soluciones y la actualización de feromonas:

```bash
python tests.py
```
---

### D. Generación de Gráficos (`graficar.py`)
Para generar la visualización de la ruta a partir de los resultados:

```bash
python graficar.py resultados/resultados.csv
```

* **Salida:** Las imágenes se guardan de forma automática en la carpeta `graficos/` identificadas por experimento (por ejemplo, `graficos/grafico_exp01_s12345_h50_c7544.png`).

---

## 4. Parámetros del Algoritmo

* **Número de iteraciones:** entre 100 y 500.
* **Número de hormigas:** entre 10 y 100.
* **Factor de evaporación ($\alpha$):** 0.1.
* **Coeficiente heurístico ($\beta$):** 2.5 (rango entre 2 y 5).
* **Probabilidad límite de explotación ($q_0$):** 0.9.

---

## 5. Formulación Matemática (TSP)

* **Información heurística (visibilidad):**
  $$\eta_{ij} = \frac{1}{d_{ij}}$$

* **Feromona inicial ($\tau_0$):**
  $$\tau_0 = \frac{1}{n \cdot L_{nn}}$$
  *(donde $n$ es el número de ciudades y $L_{nn}$ es el costo de una solución generada por vecino más cercano o aleatoria).*

* **Actualización global de feromona:**
  $$\tau_{ij} \leftarrow (1 - \alpha) \cdot \tau_{ij} + \alpha \cdot \Delta \tau_{ij}$$
  $$\Delta \tau_{ij} = \frac{1}{L_{gb}}$$
  *(aplicada exclusivamente sobre las aristas pertenecientes a la mejor ruta global $L_{gb}$).*

---

## 6. Conjunto de Pruebas y Objetivo

* **Instancia:** `berlin52.tsp.txt` (52 ciudades en Alemania).
* **Valor óptimo de referencia:** 7542 (distancia entera redondeada TSPLIB) / 7544.37 (distancia euclidiana real).
* **Objetivo:** Encontrar una ruta de longitud mínima que visite cada ciudad exactamente una vez y retorne a la ciudad de origen.

---

## 7. Formato del Archivo de Resultados (`resultados.csv`)

El archivo de salida almacena la información estructurada de las corridas para su posterior procesamiento:
* `Instancia`: Nombre o ruta del archivo evaluado.
* `Semilla`: Semilla aleatoria utilizada para reproducibilidad.
* `Hormigas`, `Iteraciones`, `Evaporacion`, `Beta`, `q0`: Hiperparámetros de la ejecución.
* `Mejor_Costo`: Distancia mínima encontrada por el algoritmo.
* `Iteracion_Mejor`: Iteración exacta en la que se halló la mejor solución.
* `Tiempo_CPU`: Tiempo de procesamiento en segundos.
* `Ruta`: Secuencia ordenada de ciudades visitadas separadas por guiones.

---
## 8. Resumen del Mejor Resultado Obtenido

Tras ejecutar la batería de pruebas experimentales, el algoritmo alcanzó con éxito el valor óptimo global de la instancia:

* **Mejor Costo alcanzado:** 7544.37 (Óptimo global TSPLIB)
* **Configuración óptima:** 50 hormigas, 200 iteraciones, $\alpha = 0.1$, $\beta = 2.5$, $q_0 = 0.9$, semilla `12345`.
* **Archivo gráfico asociado:** `graficos/grafico_exp01_s12345_h50_c7544.png`
* **Tiempo de cómputo promedio:** ~1.5 a 3.0 segundos de CPU.
* **Comportamiento observado:** La combinación de explotación intensiva ($q_0 = 0.9$) con evaporación local rápida permitió evitar mínimos locales tempranos, alcanzando una convergencia consistente y óptima en múltiples ejecuciones.

----

## 9. Transferencia a un Problema Más Complejo (PFSP)

Respuestas al análisis formativo de transferencia metodológica hacia el *Permutation Flow Shop Scheduling Problem* (PFSP):

### 1. ¿Qué partes de `acs.py` podrían mantenerse?
* **Estructura general de control:** El ciclo por iteraciones, la gestión de colonias, la construcción paso a paso de soluciones por parte de cada hormiga y la actualización de la mejor solución global encontrada.
* **Mecanismos de toma de decisiones de ACS:** La regla de selección pseudo-aleatoria proporcional ponderada por $q_0$, la regla de evaporación local de feromonas para favorecer la diversificación y el depósito global de feromonas reservado para la mejor solución histórica.

### 2. ¿Qué operaciones de `operadores.py` deberían modificarse o reemplazarse?
* **Lectura de datos:** Se reemplaza la lectura de coordenadas bidimensionales $(x, y)$ por una función que lea matrices de tiempos de procesamiento $p_{i,j}$ para $n$ trabajos en $m$ máquinas.
* **Información heurística ($\eta_{ij}$):** El inverso de la distancia ($1/d_{ij}$) deja de tener sentido físico. Debe reemplazarse por heurísticas de ordenamiento de producción, como la regla de menor tiempo de procesamiento total (SPT) o indicadores derivados del algoritmo NEH.
* **Función de costo:** Se elimina la distancia euclidiana del ciclo y se implementa el cómputo del Makespan ($C_{\max}$).
* **Estructura de feromonas:** En lugar de asociar la feromona a aristas geométricas entre ciudades, se modela la conveniencia de programar un trabajo $j$ inmediatamente a continuación del trabajo $i$, o bien la asignación del trabajo $j$ a la posición $k$ de la secuencia.

### 3. ¿Qué nueva información necesitaría representar una solución?
* En TSP, la solución es un recorrido cíclico cerrado con retorno obligatorio a la ciudad de origen.
* En PFSP, la solución es una **permutación lineal** $\pi = (\pi_1, \pi_2, \dots, \pi_n)$ de $n$ trabajos. Representa el orden único en el que las piezas ingresan secuencialmente a cada una de las $m$ máquinas del taller (sin ciclo de retorno).

### 4. ¿Qué cambiaría en la función que evalúa una solución?
* En TSP, la evaluación consiste en una sumatoria de distancias geométricas consecutivas.
* En PFSP, la evaluación requiere calcular los instantes de finalización $C(i, j)$ de cada trabajo $i$ en cada máquina $j$ considerando esperas y bloqueos, mediante la relación recursiva:
  $$C(i, j) = \max(C(i-1, j), C(i, j-1)) + p_{\pi_i, j}$$
  con condiciones iniciales $C(0, j) = 0$ y $C(i, 0) = 0$.
* La métrica a minimizar es el **Makespan**, que corresponde al tiempo total requerido para terminar todos los trabajos en la última máquina:
  $$C_{\max}(\pi) = C(n, m)$$