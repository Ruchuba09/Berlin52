def imprimeGrafo(tam,sol):
    etiqueta = [x for x in range(tam)]
    lista = []
    for i in range(tam-1):
        par = []
        par.append(sol[i])
        par.append(sol[i+1])
        lista.append(par)
    lista.append([sol[-1],sol[0]])
    color = ['red']* numVariables
    color [lista[0][0]] = 'blue'
    g = ig.Graph(n = tam,directed = True)
    g.add_edges(lista)
    g.vs["label"] = etiqueta
    g.vs["color"] = color
    g.vs["label_size"] = 6
    g.vs["size"] = 12
    g.es["edge_size"] = 2
    return g
