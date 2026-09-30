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
