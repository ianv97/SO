matriz = []
cola_memoria = []

def pfijas_ff(particiones):
    cola_listos = []
    memoria_llena = True
    for n in range(cola_memoria[0], cola_memoria[0] + len(cola_memoria)):
        i = 0
        while (particiones[i][0] < cola_memoria[n]) or (particiones[i][1] != 0):
            i += 1
        if (particiones[i][0] >= matriz[n]) and (particiones[i][1] == 0):
            particiones[i][1] = n
            cola_listos.append(n)
            for a in range(len(particiones)):
                if particiones[a][1] != 0:
                    memoria_llena = False
            if memoria_llena:
                break
    return memoria_llena

def agregar_cola_memoria(tiempo):
    z = len(cola_memoria)
    while matriz[z] <= tiempo:
        cola_memoria.append(z)
        z += 1

def fcfs(particiones, alg_particiones):
    tiempo = 0
    while not fin:
        agregar_cola_memoria(tiempo)
        if particiones == 'fijas':
            if alg_particiones == 'ff':
                pfijas_ff(particiones)
            else:
                pass
        else:
            pass
