import copy
matriz_procesos = []
matriz_resultados = []
cola_memoria = []
cola_listos = []
cola_entrada = []
cola_salida = []
lista_completados = []
particiones = []
matriz_particiones = []

def agregar_cola_memoria(tiempo, prox_proceso_agregar):
    while (prox_proceso_agregar < len(matriz_procesos)) and (matriz_procesos[prox_proceso_agregar][0] <= tiempo): # Agrego procesos con tiempo de arribo menor o igual al actual
        cola_memoria.append([matriz_procesos[prox_proceso_agregar][6], prox_proceso_agregar]) # Agrego el n_proceso y la memoria que ocupa
        prox_proceso_agregar += 1
    return prox_proceso_agregar

def liberar_particion(n_proceso):
    i = 0
    while (i < len(particiones)-1) and (particiones[i][1] != n_proceso):
        i += 1
    if particiones[i][1] == n_proceso:
        particiones[i][1] = 0

def pfijas(alg_particiones):
    memoria_llena = True
    n = 0
    while n < len(cola_memoria): # Para cada proceso en la cola de memoria
        i = 0
        if alg_particiones == 'FF':
            while i < (len(particiones)-1) and ((particiones[i][0] < cola_memoria[n][0]) or (particiones[i][1] != 0)): # Busco una partición libre con tamaño mayor al proceso en la cola
                i += 1
        else: #Best Fit
            menor_espacio = [99999, 0]  # [Tamaño, Número de partición]
            while i < len(particiones): # Busco la partición libre más chica
                if (particiones[i][1] == 0) and (particiones[i][0] < menor_espacio[0]) and (particiones[i][0] >= cola_memoria[n][0]):
                    menor_espacio = [particiones[i][0], i]
                i += 1
            i = menor_espacio[1]
        if (particiones[i][0] >= cola_memoria[n][0]) and (particiones[i][1] == 0):
            particiones[i][1] = cola_memoria[n][1] # Asigno a la particion el n_proceso que la ocupa
            # Cola de listos [n_proceso, casilla de cpu a descontar, ciclos de cpu]
            cola_listos.append([cola_memoria[n][1], 1, matriz_procesos[cola_memoria[n][1]][1]])
            cola_memoria.pop(n) #Elimino el proceso de la cola de memoria
        else: # Si no se eliminó un elemento de la cola de memoria, paso al siguiente proceso en la cola de memoria
            n += 1
    for a in range(len(particiones)): # Recorro todas las particiones para determinar si hay alguna libre
        if particiones[a][1] == 0:
            memoria_llena = False
            break
    return memoria_llena

def pvariables(alg_particiones):
    n = 0
    while n < len(cola_memoria): # Para cada proceso en la cola de memoria
        i = 0
        if alg_particiones == 'FF':
            while i < (len(particiones)-1) and ((particiones[i][0] < cola_memoria[n][0]) or (particiones[i][1] != 0)): # Busco una partición libre con tamaño mayor al proceso en la cola
                i += 1
        else: #Worst Fit
            mayor_espacio = [0, 0] # [Tamaño, Número de partición]
            while i < len(particiones): # Busco la partición libre más grande
                if (particiones[i][1] == 0) and (particiones[i][0] > mayor_espacio[0]):
                    mayor_espacio = [particiones[i][0], i]
                i += 1
            i = mayor_espacio[1]
        if (particiones[i][0] >= cola_memoria[n][0]) and (particiones[i][1] == 0):
            if (particiones[i][0] == cola_memoria[n][0]) and (particiones[i][1] == 0):
                # Si el tamaño de la particion libre es igual a la del proceso, la asigno al proceso sin crear otra partición
                particiones[i][1] = cola_memoria[n][1]
            else:
                # Sino, creo una nueva partición de tamaño igual al requerido por el proceso, restandole ese espacio al espacio libre de la particion contigua
                particiones[i][0] -= cola_memoria[n][0]
                particiones.insert(i, cola_memoria[n])
            # Cola de listos [n_proceso, casilla de cpu a descontar, ciclos de cpu]
            cola_listos.append([cola_memoria[n][1], 1, matriz_procesos[cola_memoria[n][1]][1]])
            cola_memoria.pop(n)  #Elimino el proceso de la cola de memoria
        else: # Si no se eliminó un elemento de la cola de memoria, paso al siguiente proceso en la cola de memoria
            n += 1

def compactacion_memoria():
    particion_a_incrementar = -1
    i = 0
    while i < len(particiones): # Para cada partición
        if particiones[i][1] == 0: # Si está libre
            if particion_a_incrementar == -1: # Y no hay una partición libre anterior a ella, resguardo el número de partición
                particion_a_incrementar = i
                i += 1
            else: # Si hay una libre anterior, elimino la partición actual y le sumo su tamaño a la anterior
                particiones[particion_a_incrementar][0] += particiones[i][0]
                particiones.pop(i)
        else:
            particion_a_incrementar = -1
            i += 1
    return True

def no_apropiativos(esquema_particiones, alg_particiones, alg_procesos):
    tiempo = 0
    prox_proceso_agregar = 1
    cpu = 0
    entrada = 0
    salida = 0
    memoria_llena = False
    cpu_aux = ''
    entrada_aux = ''
    salida_aux = ''
    while len(lista_completados) != len(matriz_procesos)-1: # Bucle principal: mientras no se terminen todos los procesos
        # Agrego procesos a la cola de memoria
        prox_proceso_agregar = agregar_cola_memoria(tiempo, prox_proceso_agregar)
        # Cargo los procesos de la cola en memoria
        if esquema_particiones == 'FIJAS':
            if not memoria_llena:
                memoria_llena = pfijas(alg_particiones)
        else: # Particiones variables
            if not memoria_llena: # Cuando se termina un proceso (memoria_llena se pone en False), compacto la memoria
                memoria_llena = compactacion_memoria()
            pvariables(alg_particiones)

        # Strings de salida en la tabla de resultados
        e_bloqueado = ''
        c_listo = ''
        c_entrada = ''
        c_salida = ''
        for i in range(len(cola_listos)):
            c_listo += str(cola_listos[i][0]) + ', '
        for i in range(len(cola_entrada)):
            c_entrada += str(cola_entrada[i][0]) + ', '
        for i in range(len(cola_salida)):
            c_salida += str(cola_salida[i][0]) + ', '
        if entrada != 0:
            e_bloqueado += str(entrada) + ', '
        if salida != 0:
            e_bloqueado += str(salida) + ', '
        e_bloqueado += c_entrada + c_salida

        # Si la cpu está libre y hay procesos en la cola de listos, le asigno la cpu al primero y lo saco de la cola de listos
        if (cpu == 0) and (len(cola_listos) > 0):
            if alg_procesos == 'FCFS':
                indice = 0
            else: #SJF
                indice = cola_listos.index(min(cola_listos, key = lambda listos: listos[2]))
            cpu = cola_listos[indice][0]
            cpu_aux = str(cpu)
            casilla_cpu = cola_listos[indice][1]
            cola_listos.pop(indice)
        # Si la cpu está asignada a un proceso, descuento 1 al tiempo de cpu restante
        if cpu != 0:
            matriz_procesos[cpu][casilla_cpu] -= 1
            # Si el proceso no tiene mas tiempo de cpu, lo agrego a otra cola y pongo en 0 la cpu
            if matriz_procesos[cpu][casilla_cpu] == 0:
                if matriz_procesos[cpu][2] > 0:
                    cola_entrada.append([cpu, matriz_procesos[cpu][2]])
                    cpu = 0
                elif matriz_procesos[cpu][3] > 0:
                    casilla_cpu = 3
                elif matriz_procesos[cpu][4] > 0:
                    cola_salida.append([cpu, matriz_procesos[cpu][4]])
                    cpu = 0
                elif matriz_procesos[cpu][5] > 0:
                    casilla_cpu = 5
                else: # Si tod0 está en 0 lo agrego a la lista de procesos completados y libero la memoria
                    lista_completados.append(cpu)
                    liberar_particion(cpu)
                    memoria_llena = False
                    cpu = 0
        else:
            cpu_aux = ''

        # Si la entrada está libre y hay procesos en la cola de entrada, le asigno la entrada al primero y lo saco de la cola de entrada
        if (entrada == 0) and (len(cola_entrada) > 0):
            hay_procesos = True
            if alg_procesos == 'FCFS':
                indice = 0
            else: # SJF
                indice = cola_entrada.index(min(cola_entrada, key = lambda ent: ent[1]))

                if str(cola_entrada[indice][0]) == cpu_aux:  # Si el índice corresponde al proceso que recién terminó cpu, busco otro índice
                    cola_entrada_aux = copy.deepcopy(cola_entrada)
                    cola_entrada_aux.pop(indice)
                    if len(cola_entrada_aux) > 0:
                        indice = cola_entrada.index(min(cola_entrada_aux, key=lambda ent: ent[1]))
                    else:
                        hay_procesos = False

            if hay_procesos and (str(cola_entrada[indice][0]) != cpu_aux): # Si el proceso en la cola de entrada no es el que se agregó recién
                entrada = cola_entrada[indice][0]
                entrada_aux = str(entrada)
                cola_entrada.pop(indice)
        # Si la entrada está asignada a un proceso, descuento 1 al tiempo de entrada restante
        if entrada != 0:
            matriz_procesos[entrada][2] -= 1
            # Si el proceso no tiene mas tiempo de entrada, lo agrego a otra cola y pongo en 0 la entrada
            if matriz_procesos[entrada][2] == 0:
                if matriz_procesos[entrada][3] > 0:
                    cola_listos.append([entrada, 3, matriz_procesos[entrada][3]])
                elif matriz_procesos[entrada][4] > 0:
                    cola_salida.append([entrada, matriz_procesos[entrada][4]])
                elif matriz_procesos[entrada][5] > 0:
                    cola_listos.append([entrada, 5, matriz_procesos[entrada][5]])
                entrada = 0
        else:
            entrada_aux = ''

        # Si la salida está libre y hay procesos en la cola de salida, le asigno la salida al primero y lo saco de la cola de salida
        if (salida == 0) and (len(cola_salida) > 0):
            hay_procesos = True
            if alg_procesos == 'FCFS':
                indice = 0
            else: # SJF
                indice = cola_salida.index(min(cola_salida, key = lambda sal: sal[1]))

                if (str(cola_salida[indice][0]) == cpu_aux) or str(cola_salida[indice][0]) == entrada_aux:  # Si el índice corresponde al proceso que recién terminó cpu o entrada, busco otro índice
                    cola_salida_aux = copy.deepcopy(cola_salida)
                    cola_salida_aux.pop(indice)
                    if len(cola_salida_aux) > 0:
                        indice = cola_salida.index(min(cola_salida_aux, key=lambda ent: ent[1]))
                        if (str(cola_salida[indice][0]) == cpu_aux) or str(cola_salida[indice][0]) == entrada_aux:  # Si el índice corresponde al proceso que recién terminó cpu o entrada, busco otro índice
                            cola_salida_aux.pop(indice)
                            if len(cola_salida_aux) > 0:
                                indice = cola_salida.index(min(cola_salida_aux, key=lambda ent: ent[1]))
                            else:
                                hay_procesos = False
                    else:
                        hay_procesos = False

            if hay_procesos and (str(cola_salida[indice][0]) != cpu_aux) and (str(cola_salida[indice][0]) != entrada_aux): # Si el proceso en la cola de salida no es el que se agregó recién
                salida = cola_salida[indice][0]
                salida_aux = str(salida)
                cola_salida.pop(indice)
        # Si la salida está asignada a un proceso, descuento 1 al tiempo de salida restante
        if salida != 0:
            matriz_procesos[salida][4] -= 1
            if matriz_procesos[salida][4] == 0: # Si el proceso no tiene más tiempo de salida, lo agrego a la cola de cpu(5) y pongo en 0 la salida
                cola_listos.append([salida, 5, matriz_procesos[salida][5]])
                salida = 0
        else:
            salida_aux = ''

        matriz_resultados.append([str(tiempo), c_listo[:-2], e_bloqueado[:-2], str(cpu_aux), c_listo[:-2], c_entrada[:-2], c_salida[:-2], cpu_aux, entrada_aux, salida_aux])
        matriz_particiones.append(copy.deepcopy(particiones))
        tiempo += 1


def apropiativos(esquema_particiones, alg_particiones, alg_procesos, quantum=0):
    tiempo = 0
    prox_proceso_agregar = 1
    cpu = 0
    entrada = 0
    salida = 0
    memoria_llena = False
    casilla_cpu = 1
    cpu_aux = ''
    entrada_aux = ''
    salida_aux = ''
    quantum_cpu = 0
    quantum_entrada = 0
    quantum_salida = 0
    while len(lista_completados) != len(matriz_procesos) - 1:  # Bucle principal: mientras no se terminen todos los procesos
        e_bloqueado = ''
        c_listo = ''
        c_entrada = ''
        c_salida = ''
        prox_proceso_agregar = agregar_cola_memoria(tiempo, prox_proceso_agregar)  # Agrego procesos a la cola de memoria
        # Cargo los procesos de la cola en memoria
        if esquema_particiones == 'FIJAS':
            if not memoria_llena:
                memoria_llena = pfijas(alg_particiones)
        else:  # Particiones variables
            if not memoria_llena:  # Cuando se termina un proceso (memoria_llena se pone en False), compacto la memoria
                memoria_llena = compactacion_memoria()
            pvariables(alg_particiones)

        # Strings de salida en la tabla de resultados
        for i in range(len(cola_listos)):
            c_listo += str(cola_listos[i][0]) + ', '
        for i in range(len(cola_entrada)):
            c_entrada += str(cola_entrada[i][0]) + ', '
        for i in range(len(cola_salida)):
            c_salida += str(cola_salida[i][0]) + ', '
        if entrada != 0:
            e_bloqueado += str(entrada) + ', '
        if salida != 0:
            e_bloqueado += str(salida) + ', '
        e_bloqueado += c_entrada + c_salida


        if len(cola_listos) > 0:
            if alg_procesos == 'SRTF':
                indice = cola_listos.index(min(cola_listos, key=lambda listos: listos[2]))
                if cola_listos[indice][2] < matriz_procesos[cpu][casilla_cpu]:  # Si hay un proceso en la cola de listos con tiempo restante menor al que se estaba ejecutando, le asigno la cpu
                    if cpu != 0: # Si la cpu no es el proceso 0, lo agrego nuevamente a la cola de listos (proceso que no terminó)
                        cola_listos.append([cpu, casilla_cpu, matriz_procesos[cpu][casilla_cpu]])
                    cpu = cola_listos[indice][0]
                    cpu_aux = str(cpu)
                    casilla_cpu = cola_listos[indice][1]
                    cola_listos.pop(indice)
            elif alg_procesos == 'RR':
                if quantum_cpu <= 0:  # Si se terminó el quantum
                    if cpu != 0: # Si la cpu no es el proceso 0, lo agrego nuevamente a la cola de listos (proceso que no terminó)
                        cola_listos.append([cpu, casilla_cpu, matriz_procesos[cpu][casilla_cpu]])
                    cpu = cola_listos[0][0]
                    quantum_cpu = quantum
                    cpu_aux = str(cpu)
                    casilla_cpu = cola_listos[0][1]
                    cola_listos.pop(0)
        if cpu != 0:  # Si la cpu está asignada a un proceso, descuento 1 al tiempo de cpu restante
            matriz_procesos[cpu][casilla_cpu] -= 1
            quantum_cpu -= 1
            if matriz_procesos[cpu][casilla_cpu] == 0:  # Si el proceso no tiene mas tiempo de cpu, lo agrego a otra cola y pongo en 0 la cpu
                if matriz_procesos[cpu][2] > 0:
                    cola_entrada.append([cpu, matriz_procesos[cpu][2]])
                    cpu = 0
                    quantum_cpu = 0
                elif matriz_procesos[cpu][3] > 0:
                    casilla_cpu = 3
                elif matriz_procesos[cpu][4] > 0:
                    cola_salida.append([cpu, matriz_procesos[cpu][4]])
                    cpu = 0
                    quantum_cpu = 0
                elif matriz_procesos[cpu][5] > 0:
                    casilla_cpu = 5
                else:  # Si tod0 está en 0 lo agrego a la lista de procesos completados y libero la memoria
                    lista_completados.append(cpu)
                    liberar_particion(cpu)
                    memoria_llena = False
                    cpu = 0
                    quantum_cpu = 0
        else:
            cpu_aux = ''


        if len(cola_entrada) > 0:
            if alg_procesos == 'SRTF':
                indice = cola_entrada.index(min(cola_entrada, key=lambda ent: ent[1]))

                hay_procesos = True
                if str(cola_entrada[indice][0]) == cpu_aux:  # Si el índice corresponde al proceso que recién terminó cpu, busco otro índice
                    cola_entrada_aux = copy.deepcopy(cola_entrada)
                    cola_entrada_aux.pop(indice)
                    if len(cola_entrada_aux) > 0:
                        indice = cola_entrada.index(min(cola_entrada_aux, key=lambda ent: ent[1]))
                    else:
                        hay_procesos = False

                # Si hay un proceso en la cola de entrada con tiempo restante menor al que se estaba ejecutando, le asigno la entrada
                if hay_procesos and (cola_entrada[indice][1] < matriz_procesos[entrada][2]):
                    if entrada != 0: # Si la entrada no es el proceso 0, lo agrego nuevamente a la cola de entrada (proceso que no terminó)
                        cola_entrada.append([entrada, matriz_procesos[entrada][2]])
                    entrada = cola_entrada[indice][0]
                    entrada_aux = str(entrada)
                    cola_entrada.pop(indice)

            elif alg_procesos == 'RR' and (quantum_entrada <= 0) and (str(cola_entrada[0][0]) != cpu_aux):
                if entrada != 0: # Si la cpu no es el proceso 0, lo agrego nuevamente a la cola de listos (proceso que no terminó)
                    cola_entrada.append([entrada, matriz_procesos[entrada][2]])
                entrada = cola_entrada[0][0]
                quantum_entrada = quantum
                entrada_aux = str(entrada)
                cola_entrada.pop(0)
        if entrada != 0:  # Si la entrada está asignada a un proceso, descuento 1 al tiempo de entrada restante
            matriz_procesos[entrada][2] -= 1
            quantum_entrada -= 1
            if matriz_procesos[entrada][2] == 0:  # Si el proceso no tiene mas tiempo de entrada, lo agrego a otra cola y pongo en 0 la entrada
                if matriz_procesos[entrada][3] > 0:
                    cola_listos.append([entrada, 3, matriz_procesos[entrada][3]])
                elif matriz_procesos[entrada][4] > 0:
                    cola_salida.append([entrada, matriz_procesos[entrada][4]])
                elif matriz_procesos[entrada][5] > 0:
                    cola_listos.append([entrada, 5, matriz_procesos[entrada][5]])
                entrada = 0
                quantum_entrada = 0
        else:
            entrada_aux = ''


        if len(cola_salida) > 0:
            if alg_procesos == 'SRTF':
                indice = cola_salida.index(min(cola_salida, key=lambda sal: sal[1]))

                hay_procesos = True
                if (str(cola_salida[indice][0]) == cpu_aux) or str(cola_salida[indice][0]) == entrada_aux:  # Si el índice corresponde al proceso que recién terminó cpu o entrada, busco otro índice
                    cola_salida_aux = copy.deepcopy(cola_salida)
                    cola_salida_aux.pop(indice)
                    if len(cola_salida_aux) > 0:
                        indice = cola_salida.index(min(cola_salida_aux, key=lambda ent: ent[1]))
                        if (str(cola_salida[indice][0]) == cpu_aux) or str(cola_salida[indice][0]) == entrada_aux:  # Si el índice corresponde al proceso que recién terminó cpu o entrada, busco otro índice
                            cola_salida_aux.pop(indice)
                            if len(cola_salida_aux) > 0:
                                indice = cola_salida.index(min(cola_salida_aux, key=lambda ent: ent[1]))
                            else:
                                hay_procesos = False
                    else:
                        hay_procesos = False

                # Si hay un proceso en la cola de entrada con tiempo restante menor al que se estaba ejecutando, le asigno la entrada
                if hay_procesos and (cola_salida[indice][1] < matriz_procesos[salida][4]):
                    if salida != 0: # Si la salida no es el proceso 0, lo agrego nuevamente a la cola de salida (proceso que no terminó)
                        cola_salida.append([salida, matriz_procesos[salida][2]])
                    salida = cola_salida[indice][0]
                    salida_aux = str(salida)
                    cola_salida.pop(indice)

            elif alg_procesos == 'RR' and (quantum_salida <= 0) and (str(cola_salida[0][0]) != cpu_aux) and (str(cola_salida[0][0]) != entrada_aux):
                if salida != 0: # Si la cpu no es el proceso 0, lo agrego nuevamente a la cola de listos (proceso que no terminó)
                    cola_salida.append([salida, matriz_procesos[salida][2]])
                salida = cola_salida[0][0]
                quantum_salida = quantum
                salida_aux = str(salida)
                cola_salida.pop(0)
        if salida != 0:  # Si la salida está asignada a un proceso, descuento 1 al tiempo de salida restante
            matriz_procesos[salida][4] -= 1
            quantum_salida -= 1
            if matriz_procesos[salida][4] == 0:  # Si el proceso no tiene mas tiempo de salida, lo agrego a la cola de cpu(5) y pongo en 0 la salida
                cola_listos.append([salida, 5, matriz_procesos[salida][5]])
                salida = 0
                quantum_salida = 0
        else:
            salida_aux = ''

        matriz_resultados.append([str(tiempo), c_listo[:-2], e_bloqueado[:-2], str(cpu_aux), c_listo[:-2], c_entrada[:-2], c_salida[:-2], cpu_aux, entrada_aux, salida_aux])
        matriz_particiones.append(copy.deepcopy(particiones))
        tiempo += 1
        # print(particiones)
        # print(cola_memoria)
        # print(matriz_procesos)