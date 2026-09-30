#6 Immprimir informacion de los datos leidos

matrizCoordenadas = pd.read_table(entrada, header=None,sep=r'\s+',skiprows=6,skipfooter=2)
matrizCoordenadas = matrizCoordenadas.drop(columns=0).to_numpy()
print('matriz de coordenadas: ', matrizCoordenadas.shape)
numVariables = matrizCoordenadas.shape[0]
print('Matriz de coordenadas: \n', matrizCoordenadas,'\ntamaño:',matrizCoordenadas.shape,'\ntipo:',type(matrizCoordenadas))
print('Numero de variables: ', numVariables)

#Para esto se utiliza la formula de distancia

matrizDistancias = mp.full((numVariables,numVariables),fill_value=-1.0,dtype=float)
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

