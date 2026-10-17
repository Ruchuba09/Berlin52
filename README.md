# Berlin52 - Anteproyecto Tarea 2

Implementación del algoritmo Sistema de Colonia de Hormigas (*Ant Colony System*, ACS) aplicado al Problema del Vendedor Viajero (TSP) sobre la instancia estándar Berlin52.

---

## 1. Parámetros del Algoritmo

* **Número de iteraciones:** entre 100 y 500
* **Número de hormigas:** entre 10 y 100
* **Factor de evaporación ($\alpha$):** 0.1
* **Coeficiente heurístico ($\beta$):** 2.5 (rango entre 2 y 5)
* **Probabilidad límite de explotación ($q_0$):** 0.9

---

## 2. Formulación Matemática (TSP)

* **Información heurística (visibilidad):**
  $$\eta_{ij} = \frac{1}{d_{ij}}$$

* **Feromona inicial ($\tau_0$):**
  $$\tau_0 = \frac{1}{n \cdot L_{nn}}$$
  *(donde $n$ es el número de ciudades y $L_{nn}$ es el costo de una solución generada por vecino más cercano o inicial).*

* **Actualización global de feromona:**
  $$\tau_{ij} \leftarrow (1 - \alpha) \cdot \tau_{ij} + \alpha \cdot \Delta \tau_{ij}$$
  $$\Delta \tau_{ij} = \frac{1}{L_{gb}}$$
  *(depositada exclusivamente sobre los arcos pertenecientes a la mejor ruta global $L_{gb}$).*

---

## 3. Conjunto de Pruebas y Objetivo

* **Instancia:** `berlin52.tsp.txt` (52 ciudades en Alemania).
* **Valor óptimo de referencia:** 7542 (distancia entera redondeada TSPLIB) / 7544.37 (distancia euclidiana real).
* **Objetivo:** Encontrar una ruta de longitud mínima que visite cada ciudad exactamente una vez y retorne a la ciudad de origen.

---

## 4. Transferencia a un Problema Más Complejo (PFSP)

Respuestas al análisis de transferencia metodológica hacia el *Permutation Flow Shop Scheduling Problem* (PFSP):

### 1. ¿Qué partes de `acs.py` podrían mantenerse?
* **Arquitectura de control del flujo:** Se mantiene intacto el ciclo principal de iteraciones: inicialización de estructuras, construcción iterativa de soluciones por cada hormiga, evaluación de la población de hormigas y preservación de la mejor solución global encontrada.
* **Mecanismos propios de ACS:** Se conserva la regla de decisión pseudo-aleatoria proporcional basada en el parámetro $q_0$ (balance entre explotación voraz y exploración probabilística), la regla de evaporación local paso a paso para diversificar la búsqueda, y el refuerzo de feromona global exclusivo para la mejor solución de la iteración o global.

### 2. ¿Qué operaciones de `operadores.py` deberían modificarse o reemplazarse?
* **Lectura de datos:** Se reemplaza el parser de coordenadas cartesianas $(x, y)$ por una función capaz de leer una matriz de tiempos de procesamiento $p_{i,j}$ para $n$ trabajos distribuidos en $m$ máquinas.
* **Información heurística ($\eta_{ij}$):** Debe sustituirse el inverso de la distancia euclidiana ($1/d_{ij}$) por una métrica coherente con scheduling, como la regla de menor tiempo de procesamiento total (SPT, *Shortest Processing Time*) o la visibilidad basada en el orden heurístico de NEH.
* **Función de costo:** Se elimina el cómputo de distancia euclidiana acumulada y se incorpora el evaluador del Makespan ($C_{\max}$).
* **Grafo de transiciones:** La matriz de feromona ya no conecta ciudades geográficas, sino la asignación secuencial del trabajo $j$ programado inmediatamente después del trabajo $i$.

### 3. ¿Qué nueva información necesitaría representar una solución?
* En el TSP, una solución representa una ruta o ciclo hamiltoniano cerrado de ciudades donde el retorno a la ciudad inicial es mandatorio.
* En el PFSP, una solución pasa a ser una **permutación lineal estricta** $\pi = (\pi_1, \pi_2, \dots, \pi_n)$ de $n$ trabajos. No existe concepto de retorno al origen; la solución define únicamente el orden idéntico en que los trabajos ingresan secuencialmente a cada una de las máquinas $M_1 \rightarrow M_2 \rightarrow \dots \rightarrow M_m$.

### 4. ¿Qué cambiaría en la función que evalúa una solución?
* En lugar de sumar linealmente distancias entre pares consecutivos de nodos y cerrar el ciclo con el nodo de origen, la evaluación requiere simular el avance de los trabajos a través de las máquinas mediante programación dinámica.
* Se debe calcular la matriz de tiempos de finalización $C(i, j)$ para cada posición $i$ de la secuencia ($1 \le i \le n$) y cada máquina $j$ ($1 \le j \le m$) según la ecuación recursiva:
  $$C(i, j) = \max(C(i-1, j), C(i, j-1)) + p_{\pi_i, j}$$
  con condiciones de borde $C(0, j) = 0$ y $C(i, 0) = 0$.
* La función de aptitud deja de ser la distancia total y pasa a ser el **Makespan**, correspondiente al tiempo en que el último trabajo termina en la última máquina:
  $$C_{\max}(\pi) = C(n, m)$$