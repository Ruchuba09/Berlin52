# Berlin52
Anteproyecto Tarea2


Ant Colony Systems
Parámetros:

Número de iteraciones: entre 100 y 500
Número de hormigas: entre 10 y 100
Factor de evaporación \alpha: 0.1
Coeficiente heurístico \beta: 2.5 (valor entre 2 y 5)
q_0=0.9


Formulas:

$$
\eta = \frac{1}{D_{ij}}
$$

$$
\tau^0_{ij} =
\frac{1}{NumVariables \times Costo(solucion_{inicial})}
$$

$$
\Delta =
\frac{Costo(solucion_{mejor})}{Costo(solucion_{mejor})}
$$

Conjunto de pruebas:

Berlin52
Valor óptimo: 7542 (entero), 7544,3659 (real)
Objetivo:

Minimizar la distancia viajada entre los 52 puntos como en el problema del vendedor viajero
