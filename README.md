# Berlin52 - Sistema de Colonia de Hormigas (ACS) en TSP

Implementación modular de la metaheurística Sistema de Colonia de Hormigas (*Ant Colony System*, ACS) aplicada al Problema del Vendedor Viajero (TSP) sobre la instancia estándar Berlin52.

---

## 1. Requisitos e Instalación

Para ejecutar este proyecto se requiere Python 3.8 o superior y las siguientes bibliotecas:

```bash
pip install numpy pandas matplotlib
```

---

## 2. Estructura del Proyecto

El repositorio sigue una organización modular con separación de responsabilidades:

```text
Berlin52-main/
├── acs.py                 # Orquestador principal del algoritmo ACS
├── operadores.py          # Biblioteca de funciones (distancias, heurística, feromonas)
├── tests.py               # Casos de prueba automatizados de los operadores
├── graficar.py            # Generación de gráficos a partir de los resultados
├── datos/
│   └── berlin52.tsp.txt   # Instancia de coordenadas de ciudades
├── resultados/
│   └── resultados.csv     # Archivo estructurado con los resultados experimentales
├── graficos/
│   └── grafico1.png       # Trazado de la ruta encontrada
└── README.md              # Documentación y guía de uso
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

### B. Ejecución de Pruebas Unitarias (`tests.py`)
Para comprobar el funcionamiento de la lectura de archivos, el cálculo de matrices y la validez de las soluciones generadas:

```bash
python tests.py
```

---

### C. Generación del Gráfico de la Ruta (`graficar.py`)
Para procesar el archivo CSV de salida y graficar la ruta sobre el plano cartesiano:

```bash
python graficar.py resultados/resultados.csv
```

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
  *(aplicada exclusivamente sobre las aristas de la mejor ruta global $L_{gb}$).*

---

## 6. Conjunto de Pruebas y Objetivo

* **Instancia:** `berlin52.tsp.txt` (52 ciudades en Alemania).
* **Valor óptimo de referencia:** 7542 (distancia entera redondeada TSPLIB) / 7544.37 (distancia euclidiana real).
* **Objetivo:** Encontrar una ruta de longitud mínima que visite cada ciudad exactamente una vez y retorne a la ciudad de origen.

---

## 7. Formato del Archivo de Resultados (`resultados.csv`)

El archivo de salida almacena la información necesaria para el análisis posterior:
* `Instancia`: Nombre o ruta del archivo evaluado.
* `Semilla`: Semilla aleatoria utilizada.
* `Hormigas`, `Iteraciones`, `Evaporacion`, `Beta`, `q0`: Hiperparámetros de la ejecución.
* `Mejor_Costo`: Distancia mínima encontrada.
* `Iteracion_Mejor`: Iteración en la que se halló la mejor solución.
* `Tiempo_CPU`: Tiempo de procesamiento en segundos.
* `Ruta`: Secuencia ordenada de ciudades visitadas.

---

## 8. Transferencia a un Problema Más Complejo (PFSP)

Respuestas al análisis de transferencia metodológica hacia el *Permutation Flow Shop Scheduling Problem* (PFSP):

### 1. ¿Qué partes de `acs.py` podrían mantenerse?
* **Arquitectura de control del flujo:** Se mantiene el ciclo principal de iteraciones, la inicialización de estructuras, la construcción iterativa de soluciones por hormiga y el registro de la mejor solución global.
* **Mecanismos propios de ACS:** Se conserva la regla de decisión pseudo-aleatoria proporcional ($q_0$), la regla de evaporación local para diversificar la búsqueda y el refuerzo de feromona global exclusivo para la mejor solución.

### 2. ¿Qué operaciones de `operadores.py` deberían modificarse o reemplazarse?
* **Lectura de datos:** Se sustituye el parser de coordenadas cartesianas $(x, y)$ por una función que lea una matriz de tiempos de procesamiento $p_{i,j}$ para $n$ trabajos en $m$ máquinas.
* **Información heurística ($\eta_{ij}$):** Se reemplaza el inverso de la distancia euclidiana ($1/d_{ij}$) por métricas de scheduling, como la regla de menor tiempo de procesamiento total (SPT) o visibilidad basada en NEH.
* **Función de costo:** Se elimina la distancia euclidiana acumulada y se incorpora el cálculo del Makespan ($C_{\max}$).
* **Grafo de transiciones:** La feromona conecta ahora la programación del trabajo $j$ inmediatamente después del trabajo $i$.

### 3. ¿Qué nueva información necesitaría representar una solución?
* En TSP, la solución representa un ciclo cerrado de ciudades visitadas con retorno obligatorio al origen.
* En PFSP, la solución es una **permutación lineal estricta** $\pi = (\pi_1, \pi_2, \dots, \pi_n)$ de $n$ trabajos, representando el orden idéntico en que entran secuencialmente a cada una de las máquinas (sin retorno al origen).

### 4. ¿Qué cambiaría en la función que evalúa una solución?
* En lugar de sumar distancias geométricas consecutivas, se calcula la matriz de finalización $C(i, j)$ mediante la relación recursiva:
  $$C(i, j) = \max(C(i-1, j), C(i, j-1)) + p_{\pi_i, j}$$
  con condiciones de borde $C(0, j) = 0$ y $C(i, 0) = 0$.
* El costo a minimizar pasa a ser el **Makespan**, correspondiente al tiempo en que el último trabajo termina en la última máquina:
  $$C_{\max}(\pi) = C(n, m)$$