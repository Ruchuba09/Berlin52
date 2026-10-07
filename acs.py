import sys
import time
import numpy as np
import pandas as pd
import igraph as ig

#Tiene parametros de entrada: semilla, tamaño de la colonia, numero iteraciones, tasa de evaporacion, beta,q0, datos de entrada

print('-Numero de semilla: ')
print('-Tamaño de la colonia: ')
print('-Numero de iteraciones: ')
print('-Tasa de evaporacion: ')
print('-Beta: ')
print('-Q0: ')
print('-Datos de entrada: ')
sys.exit(0)

tiempo_proceso_ini = time.process_time()

np.random.seed(semilla)

matrizDistancias = np.full((numVariables,numVariables),fill_value=-1.0,dtype=float)
for i in range (numVariables-1):
    for j in range(i+1,numVariables):
        matrizDistancias[i,j] = np.sqrt(np.sum(np.square(matrizCoordenadas[i]-matrizCoordenadas[j])))
        matrizDistancias[j,i] = matrizDistancias[i,j]
print('Matriz de Distancias: \n', matrizDistancias,'\ntamaño:',matrizDistancias.shape,'\ntipo:',type(matrizDistancias))

def solucionCalculoCosto(n,s,c):
    aux = c[s[n-1],s[0]]
    for i in range(n-1):
        aux += c[s[i],s[i+1]]
    return aux



tij0 =1/(numVariables*solucionMejorCosto)
matrizFeromonas = np.full((numVariables,numVariables),fill_value=tij0,dtype=float)
print('Matriz de Feromonas: \n', matrizFeromonas,'\ntamaño:',matrizFeromonas.shape,'\ntipo:',type(matrizFeromonas))



#6 Immprimir informacion de los datos leidos

matrizCoordenadas = pd.read_table(entrada, header=None,sep=r'\s+',skiprows=6,skipfooter=2)
matrizCoordenadas = matrizCoordenadas.drop(columns=0).to_numpy()
print('matriz de coordenadas: ', matrizCoordenadas.shape)
numVariables = matrizCoordenadas.shape[0]
print('Matriz de coordenadas: \n', matrizCoordenadas,'\ntamaño:',matrizCoordenadas.shape,'\ntipo:',type(matrizCoordenadas))
print('Numero de variables: ', numVariables)

#Para esto se utiliza la formula de distancia

matrizDistancias = np.full((numVariables,numVariables),fill_value=-1.0,dtype=float)
for i in range(numVariables-1):
    for j in range(i+1,numVariables):
        matrizDistancias[i,j] = np.sqrt(np.sum(np.square(matrizCoordenadas[i]-matrizCoordenadas[j])))
        matrizDistancias[j,i] = matrizDistancias[i,j]

print('Matriz de Distancias: \n', matrizDistancias,'\ntamaño:',matrizDistancias.shape,'\ntipo:',type(matrizDistancias))

#matriz heuristica

matrizHeuristica = np.full_like(matrizDistancias,fill_value=1/matrizDistancias,dtype=float)
np.fill_diagonal(matrizHeuristica,0)
print('Matriz de Heuristica: \n', matrizHeuristica,'\ntamaño:',matrizHeuristica.shape,'\ntipo:',type(matrizHeuristica))

#Creacion de una primera solucion generada de forma random y calculo su costo

solucionOptima = np.array([0,48,31,44,18,40,7,8,9,42,32,50,10,51,13,12,46,25,26,27,11,24,3,5,14,4,23,47,37,36,39,38,35,34,33,41,43,45,49,30,29,28,22,21,20,19,17,16,15,2,1])
solucionMejor = np.arange(0,numVariables)
np.random.shuffle(solucionMejor)
solucionMejorCosto = solucionCalculoCosto(numVariables,solucionMejor,matrizDistancias)

solucionMejorIteracion =0
print ('Solucion inicial y ala vez mejor solucion: ',solucionMejor,'\ntamaño: ',solucionMejor.shape,'\ntipo: ',type(solucionMejor),'\nCosto de la solucion: ',solucionMejorCosto)
print ('Costo de la solucion inicialy a la mejor solucion: ',solucionMejorCosto)
print ('Iteracion donde se encontro la mejor solucion: ',solucionMejorIteracion)

generacion = 0
while generacion < ite and not(np.round(solucionMejorCosto,decimales))
generacion += 1
print('Generacion: ',generacion)

colonia = np.full((tamColonia,numVariables),fill_value=-1,dtype=int)

memoria = np.ones((col,numVariables),dtype=int)


for k in range(col):
    colonia[k,0] = np.random.randint(numVariables)
    memoria[k][colonia[k,0]] = 0

for i in range(numVariables-1):
    for k in range(pd.col):
        Tall = memoria[k]*matrizFeromonas[colonia[k,i],:]*np.power(matrizHeuristica[colonia[k,i],:],beta)
        if np.random.rand() < q0:
            j0= np.random.choice(np.where(Tall==Tall.max())[0])
            colonia[k,i+1] = j0
            memoria[k][j0] = 0
        else:
            ruleta = (memoria[k]*TxN)/TxN.sum(where=memoria[k].astype(bool))
            for l in range(l,numVariables):
                ruleta[l] = ruleta[l]+ruleta[l-1]
            rTiro = np.random.rand()
            for j in range(numVariables):
                if rTiro <= ruleta[j]:
                    colonia[k,i+1] = j
                    memoria[k][j] = 0
                    break
        matrizFeromonas[colonia[k][i],colonia[k,i+1]] = ((1-tev)*matrizFeromonas[colonia[k,i],colonia[k,i+1]]) + (tev*tij0)
        matrizFeromonas[colonia[k][i+1],colonia[k,i]] = matrizFeromonas[colonia[k,i],colonia[k,i+1]]

    matrizFeromonas[colonia[k][-1]][colonia[k][0]] = ((1-tev)*matrizFeromonas[colonia[k][-1],colonia[k][0]]) + (tev*tij0)
    matrizFeromonas[colonia[k][0]][colonia[k][-1]] = matrizFeromonas[colonia[k][-1],colonia[k][0]]

    for k in range(pd.col):
        solucionCosto = solucionCalculoCosto(numVariables,colonia[k],matrizDistancias)
        if solucionCosto < solucionMejorCosto:
            solucionMejorCosto = solucionCosto
            solucionMejor = colonia[k].copy()
            solucionMejorIteracion = generacion
            print('Nueva mejor solucion: ',solucionMejor,'\nCosto de la nueva mejor solucion: ',solucionMejorCosto,'\nIteracion donde se encontro la mejor solucion: ',solucionMejorIteracion)

    for i in range(numVariables-1):
        for j in range(i+1,numVariables):
            matrizFeromonas[i,j] = (1-tev)*matrizFeromonas[i,j]
            matrizFeromonas[j,i] = matrizFeromonas[i,j]
    for i in range(numVariables-1):
        matrizFeromonas[solucionMejor[i],solucionMejor[i+1]] += tev * (1/solucionMejorCosto)
        matrizFeromonas[solucionMejor[i+1],solucionMejor[i]] = matrizFeromonas[solucionMejor[i],solucionMejor[i+1]]
    matrizFeromonas[solucionMejor[-1],solucionMejor[0]] += tev * (1/solucionMejorCosto)
    matrizFeromonas[solucionMejor[0],solucionMejor[-1]] = matrizFeromonas[solucionMejor[-1],solucionMejor[0]]
    

                    
