matriz_procesos = []
matriz_resultados = []
fila_resultado = []
cola_memoria = []
cola_listos = []
cola_entrada = []
cola_salida = []

def pfijas_ff(particiones):
    memoria_llena = True
    n = 0
    while n <= len(cola_memoria):
        i = 0
        while (particiones[i][0] < cola_memoria[n][1]) or (particiones[i][1] != 0): #Busco una partición libre con tamaño mayor al proceso en la cola
            i += 1
        if (particiones[i][0] >= cola_memoria[n][1]) and (particiones[i][1] == 0):
            particiones[i][1] = cola_memoria[n][0] #Asigno a la particion el n_proceso que la ocupa
            cola_listos.append([cola_memoria[n][0], 1]) #Agrego el n_proceso y la casilla de cpu a descontar (1, 3 o 5) a la cola de listos
            cola_memoria.pop(n) #Elimino el proceso de la cola de memoria
            for a in range(len(particiones)): #Recorro todas las particiones para determinar si hay alguna libre
                if particiones[a][1] != 0:
                    memoria_llena = False
            if memoria_llena:
                break
        else: #Sumo 1 al contador si no eliminó un elemento de la cola de memoria
            n += 1
    return memoria_llena

def agregar_cola_memoria(tiempo, ultimo_proceso_agregado):
    while matriz_procesos[ultimo_proceso_agregado] <= tiempo: #Agrego procesos con tiempo de arribo menor al actual
        cola_memoria.append([ultimo_proceso_agregado, matriz_procesos[ultimo_proceso_agregado][6]]) #Agrego el n_proceso y la memoria que ocupa
        ultimo_proceso_agregado += 1
    return ultimo_proceso_agregado

def fcfs(particiones, alg_particiones):
    tiempo = 0
    ultimo_proceso_agregado = 0
    cpu = 0
    fin = False
    while not fin:
        e_listo = ''
        e_bloqueado = ''
        c_listo = ''
        c_entrada = ''
        c_salida = ''
        ultimo_proceso_agregado = agregar_cola_memoria(tiempo, ultimo_proceso_agregado)
        if particiones == 'fijas':
            if alg_particiones == 'ff':
                pfijas_ff(particiones)
            else:
                # pfijas_bf
        else:
            if alg_particiones == 'ff':
                # pvariables_ff
            else:
                # pvariables_wf
        for i in range(len(cola_listos)):
            e_listo += str(cola_listos[i]) + ', '
        for i in range(len(cola_entrada)):
            e_bloqueado += str(cola_entrada[i]) + ', '
        for i in range(len(cola_salida)):
            e_bloqueado += str(cola_salida[i]) + ', '
        if (cpu == 0) and (len(cola_listos) > 0): #Si la cpu está libre y hay procesos en la cola de listos, le asigno la cpu al primero
            cpu = cola_listos[0][0]
            casilla_cpu = [cola_listos[0][1]]
            matriz_procesos[cpu][casilla_cpu] -= 1 #Descuento 1 al tiempo de cpu restante del proceso
            if matriz_procesos[cpu][casilla_cpu] == 0: #Si el proceso no tiene mas tiempo de cpu, lo agrego a otra cola y lo saco de la cola de listos
                if matriz_procesos[cpu][2] > 0:
                    cola_entrada.append(cpu)
                    cola_listos.pop(0)
                elif matriz_procesos[cpu][3] > 0:
                    cola_listos[0][1] = 3
                elif matriz_procesos[cpu][4] > 0:
                    cola_salida.append(cpu)
                    cola_listos.pop(0)
                elif matriz_procesos[cpu][5] > 0:
                    cola_listos[0][1] = 5
        for i in range(len(cola_listos)):
            c_listo += str(cola_listos[i]) + ', '
        for i in range(len(cola_entrada)):
            c_entrada += str(cola_entrada[i]) + ', '
        for i in range(len(cola_salida)):
            c_salida += str(cola_salida[i]) + ', '
        matriz_resultados.append([tiempo, e_listo[:-1], e_bloqueado[:-1] , cpu, c_listo[:-1], c_entrada[:-1], c_salida[:-1]])
        tiempo += 1