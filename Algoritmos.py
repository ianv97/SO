matriz_procesos = [[]]
matriz_resultados = []
fila_resultado = []
cola_memoria = []
cola_listos = []
cola_entrada = []
cola_salida = []
lista_completados = []
particiones = []

def pfijas():
    memoria_llena = True
    n = 0
    while n < len(cola_memoria): #Para cada proceso en la cola de memoria
        i = 0
        while i < (len(particiones)-1) and ((particiones[i][0] < cola_memoria[n][0]) or (particiones[i][1] != 0)): #Busco una partición libre con tamaño mayor al proceso en la cola
            i += 1
        if (particiones[i][0] >= cola_memoria[n][0]) and (particiones[i][1] == 0):
            particiones[i][1] = cola_memoria[n][1] #Asigno a la particion el n_proceso que la ocupa
            cola_listos.append([cola_memoria[n][1], 1]) #Agrego el n_proceso y la casilla de cpu a descontar (1, 3 o 5) a la cola de listos
            cola_memoria.pop(n) #Elimino el proceso de la cola de memoria
        else: #Si no se eliminó un elemento de la cola de memoria, paso al siguiente proceso en la cola de memoria
            n += 1
    for a in range(len(particiones)): #Recorro todas las particiones para determinar si hay alguna libre
        if particiones[a][1] == 0:
            memoria_llena = False
            break
    return memoria_llena

def liberar_particion(n_proceso):
    i = 0
    while (particiones[i][1] != n_proceso) and (i < len(particiones)):
        i += 1
    if particiones[i][1] == n_proceso:
        particiones[i][1] = 0

def agregar_cola_memoria(tiempo, prox_proceso_agregar):
    while (prox_proceso_agregar < len(matriz_procesos)) and (matriz_procesos[prox_proceso_agregar][0] <= tiempo): #Agrego procesos con tiempo de arribo menor o igual al actual
        cola_memoria.append([matriz_procesos[prox_proceso_agregar][6], prox_proceso_agregar]) #Agrego el n_proceso y la memoria que ocupa
        prox_proceso_agregar += 1
    return prox_proceso_agregar

def ordenar_particiones(alg_particiones):
    if alg_particiones == 'bf':
        particiones.sort(key=lambda part: part[0])
    else:
        particiones.sort(key=lambda part: part[0], reverse=True)

def pvariables():
    memoria_llena = True
    n = 0
    while n < len(cola_memoria): #Para cada proceso en la cola de memoria
        i = 0
        while i < (len(particiones)-1) and ((particiones[i][0] < cola_memoria[n][0]) or (particiones[i][1] != 0)): #Busco una partición libre con tamaño mayor al proceso en la cola
            i += 1
        if (particiones[i][0] > cola_memoria[n][0]) and (particiones[i][1] == 0):
            particiones.insert(i, cola_memoria[n])
            particiones[-1][0] -= cola_memoria[n][0]

def compactacion_memoria():
    pass

def fcfs(esquema_particiones, alg_particiones):
    tiempo = 0
    prox_proceso_agregar = 1
    cpu = 0
    entrada = 0
    salida = 0
    memoria_llena = False
    cpu_aux = ''
    entrada_aux = ''
    salida_aux = ''
    if alg_particiones != 'ff':
        ordenar_particiones(alg_particiones)
    while len(lista_completados) != len(matriz_procesos)-1:
        e_bloqueado = ''
        c_listo = ''
        c_entrada = ''
        c_salida = ''
        prox_proceso_agregar = agregar_cola_memoria(tiempo, prox_proceso_agregar)
        if not memoria_llena:
            if esquema_particiones == 'fijas':
                memoria_llena = pfijas()
            else:
                if alg_particiones == 'ff':
                    pass
                    # pvariables_ff
                else:
                    pass
                    # pvariables_wf

        if entrada != 0:
            e_bloqueado += str(entrada) + ', '
        if salida != 0:
            e_bloqueado += str(salida) + ', '
        for i in range(len(cola_entrada)):
            e_bloqueado += str(cola_entrada[i]) + ', '
        for i in range(len(cola_salida)):
            e_bloqueado += str(cola_salida[i]) + ', '
        for i in range(len(cola_listos)):
            c_listo += str(cola_listos[i][0]) + ', '
        for i in range(len(cola_entrada)):
            c_entrada += str(cola_entrada[i]) + ', '
        for i in range(len(cola_salida)):
            c_salida += str(cola_salida[i]) + ', '

        if (cpu == 0) and (len(cola_listos) > 0) and (str(cola_listos[0]) != entrada_aux) and (str(cola_listos[0]) != salida_aux): #Si la cpu está libre y hay procesos en la cola de listos, le asigno la cpu al primero y lo saco de la cola de listos
            cpu = cola_listos[0][0]
            cpu_aux = str(cpu)
            casilla_cpu = cola_listos[0][1]
            cola_listos.pop(0)
        if cpu != 0: #Si la cpu está asignada a un proceso, descuento 1 al tiempo de cpu restante
            matriz_procesos[cpu][casilla_cpu] -= 1
            if matriz_procesos[cpu][casilla_cpu] == 0: #Si el proceso no tiene mas tiempo de cpu, lo agrego a otra cola y pongo en 0 la cpu
                if matriz_procesos[cpu][2] > 0:
                    cola_entrada.append(cpu)
                    cpu = 0
                elif matriz_procesos[cpu][3] > 0:
                    casilla_cpu = 3
                elif matriz_procesos[cpu][4] > 0:
                    cola_salida.append(cpu)
                    cpu = 0
                elif matriz_procesos[cpu][5] > 0:
                    casilla_cpu = 5
                else: #Si_todo está en 0 lo agrego a la lista de procesos completados y libero la memoria
                    lista_completados.append(cpu)
                    liberar_particion(cpu)
                    memoria_llena = False
                    cpu = 0
        else:
            cpu_aux = ''

        if (entrada == 0) and (len(cola_entrada) > 0) and (str(cola_entrada[0]) != cpu_aux) and (str(cola_entrada[0]) != salida_aux): #Si la entrada está libre y hay procesos en la cola de entrada, le asigno la entrada al primero y lo saco de la cola de entrada
            entrada = cola_entrada[0]
            entrada_aux = str(entrada)
            cola_entrada.pop(0)
        if entrada != 0: # Si la entrada está asignada a un proceso, descuento 1 al tiempo de entrada restante
            matriz_procesos[entrada][2] -= 1
            if matriz_procesos[entrada][2] == 0: #Si el proceso no tiene mas tiempo de entrada, lo agrego a otra cola y pongo en 0 la entrada
                if matriz_procesos[entrada][3] > 0:
                    cola_listos.append([entrada, 3])
                elif matriz_procesos[entrada][4] > 0:
                    cola_salida.append(entrada)
                elif matriz_procesos[entrada][5] > 0:
                    cola_listos.append([entrada, 5])
                entrada = 0
        else:
            entrada_aux = ''

        if (salida == 0) and (len(cola_salida) > 0) and (str(cola_salida[0]) != cpu_aux) and (str(cola_salida[0]) != entrada_aux): #Si la salida está libre y hay procesos en la cola de salida, le asigno la salida al primero y lo saco de la cola de salida
            salida = cola_salida[0]
            salida_aux = str(salida)
            cola_salida.pop(0)
        if salida != 0: # Si la salida está asignada a un proceso, descuento 1 al tiempo de salida restante
            matriz_procesos[salida][4] -= 1
            if matriz_procesos[salida][4] == 0: #Si el proceso no tiene mas tiempo de salida, lo agrego a la cola de cpu(5) y pongo en 0 la salida
                cola_listos.append([salida, 5])
                salida = 0
        else:
            salida_aux = ''

        matriz_resultados.append([str(tiempo), c_listo[:-2], e_bloqueado[:-2], str(cpu_aux), c_listo[:-2], c_entrada[:-2], c_salida[:-2], cpu_aux, entrada_aux, salida_aux])
        tiempo += 1