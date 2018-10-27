"""--------------------------------------------------------------------------
-----------------------------------------------------------------------------
-----------------------------------------------------------------------------
-----------------------------------------------------------------------------
de seguro hay muchos errores ortograficos no quiero escuchar ningun comentari
-----------------------------------------------------------------------------
-----------------------------------------------------------------------------
-----------------------------------------------------------------------------
-----------------------------------------------------------------------------"""

"""variable de proceso"""
data=[[3,1,2,3,2,1,20],[5,1,3,2,1,1,5],[0,1,3,4,3,1,50],[10,1,4,5,3,1,10],[8,1,2,4,3,1,70],[11,1,2,2,2,1,25]]
"""pos_data es una varible que lleva en que etapa se encuentra el proceso 
1= primera rafaga de cpu, 2= Entrada, etc, en 5 termina """
pos_data=[1,1,1,1,1,1]
"""tipo de memoria PFff=1 PFbf=2 PVff=3 PVwf=4"""
tipo_de_memoria=1
"""tipo de prceso FSFC=1 SJT=2 SJTS=3 RR=4"""
tipo_de_proceso=1


control_1=False
memory=[[70,-1],[20,-1]]
estado_memori= True


cola_listo_memoria=[]
cola_listo_proceso=[]

cola_S=[]
block_s=0
cola_E=[]
block_e=0
block=[]


resultado_total=[]
"""se debe resetear cada interacion"""
resultado_parcial=["-","-","-","-","-","-","-","-","-","-"]
ejecucion=0

"""ordena de menor a mayor los procesos por el tiempo de arribo"""
def bubblemM(A):
    for i in range(1,len(A)):
        for j in range(0,len(A)-i):
            if(A[j+1][0] < A[j][0]):
                aux=A[j];
                A[j]=A[j+1];
                A[j+1]=aux;

"""ordena de mayor a menor la memoria por el tamaño la utilizo para bf"""
def bubbleMm(A):
    for i in range(1,len(A)):
        for j in range(0,len(A)-i):
            if(A[j+1][0] > A[j][0]):
                aux=A[j];
                A[j]=A[j+1];
                A[j+1]=aux;

def cargar_ejecucion():
	if (len(cola_listo_proceso)==0):
		ejecutar="-"
		return
	ejecutar=cola_listo_proceso[1]

def cargar_block_S(p):
	if (p==0) and (len(cola_S)!=0):
		block_s=cola_S[1]

	
"""esta funcion recorre los datos de la matris y ve si el
tiempo de arribo de algun proceso es igual al  tiempo de ejecucion
en el caso de que lo sea lo agraga a la cola de memoria para pelear
por ocupar un espacio en ella """
def cargar_cola_listo_memoria(C):
	for x in range(len(data)):
		if (data[x][0]==tiempo):
			C.append(x)
"""carga de memoria fija tipo ff estado de memori nos dice si esta llena
en su caso no hace nada ya que no podemos cargar nada en ella"""
def pf_ff(m):
	if estado_memori and (len(cola_listo_memoria)!=0):
		for x in range(len(cola_listo_memoria)):
			cont=0
			for y in range(len(m)):
				if(m[y][1]==(-1)):
					if (m[y][0]>=data[cola_listo_memoria[x]][6]):
						m[y][1]=cola_listo_memoria[x]
						cola_listo_proceso.append(cola_listo_memoria[x])
						cola_listo_memoria.pop[x]
						cont+=1
						break
				else:
					cont+=1
		if (cont==len(m)):
			estado_memori= False
			break

"""carga de la memoria del tipo BF la ordeno de menor a mayor una vez asi
despues la trata como una FF ya que cuando el primer espacio en el que entre 
va a ser el mas apropiado en ese instante """
def pf_bf(m):
	if (not control_1):
		bubblemM(m)
	if estado_memori and (len(cola_listo_memoria)!=0):
		for x in range(len(cola_listo_memoria)):
			cont=0
			for y in range(len(m)):
				if(m[y][1]==(-1)):
					if (m[y][0]>=data[cola_listo_memoria[x]][6]):
						m[y][1]=cola_listo_memoria[x]
						cola_listo_proceso.append(cola_listo_memoria[x])
						cola_listo_memoria.pop[x]
						cont+=1
						break
				else:
					cont+=1
		if (cont==len(m)):
			estado_memori= False
			break
"""la carga de una memoria variable tipo ff la la asigno y voy agregando
a la derecha e espacio sobrante en caso de que entre justo no si parte la 
seccion y si esta llena termina el for aunque tenga mas procesos en la cola
ya que no tiene lugar la memoria"""
def pv_ff(m):
	if estado_memori and (len(cola_listo_memoria)!=0):
		for x in range(len(cola_listo_memoria)):
			cont=0
			for y in range(len(m)):
				if(m[y][1]==(-1)):
					if (m[y][0]>=data[cola_listo_memoria[x]][6]):
						aux=(m[y][0])-(data[cola_listo_memoria[x]][6])
						if aux!=0:
							m.insert((y+1),[aux,-1])
						m[y][0]=data[cola_listo_memoria[x]][6]
						m[y][1]=cola_listo_memoria[x]
						cola_listo_proceso.append(cola_listo_memoria[x])
						cola_listo_memoria.pop[x]
						cont+=1
						break
				else:
					cont+=1
			if (cont==len(m)):
				estado_memori= False
				break
"""fue el ultimo asi que ya lo hice sin muchas ganas pero lo que hace 
busca pa socion de la memoria que mejor encaje ya que se vusca la posicion
del mas chico que entra, recorre toda la memoria"""
def pv_wf(m):
	if estado_memori and (len(cola_listo_memoria)!=0):
		for x in range(len(cola_listo_memoria)):
			cont=0
			pos="-"
			hv=max(m)+1
			for y in range(len(m)):
				if(m[y][1]==(-1)):
					if (m[y][0]>=data[cola_listo_memoria[x]][6]):
						if (hv>m[y][0]):
							hv=m[y][0]
							pos=y
				else:
					cont+=1
			if (pos!="-"):
				aux=(m[pos][0])-(data[cola_listo_memoria[x]][6])
				if aux!=0:
					m.insert((pos+1),[aux,-1])
				m[pos][0]=data[cola_listo_memoria[x]][6]
				m[pos][1]=cola_listo_memoria[x]
				cola_listo_proceso.append(cola_listo_memoria[x])
				cola_listo_memoria.pop[x]
				cont+=1
			if (cont==len(m)):
				estado_memori= False
				break



"""las entrada y salida pueden ser cero ver al final """
def control_bloqueo(p,e):
	control_1=True
	if (p==2):
		cola_E.append(e)
		block_e=cola_E[1] 
		"""no estoy seguro"""
	else:
		cola_S.append(e)
		block_e=cola_S[1]
	block.append(e)


"""def salida():
	d[ejecucion][pos_data[ejecucion]]-=1
	if (d[ejecucion][pos_data[ejecucion]]==0):
		if (pos_data[ejecucion]==5):
			limpiar_memoria()
			d.pop(ejecucion)
			ejecucion= "-"
			return
		pos_data[ejecucion]=+1
		control_bloqueo(pos_data[ejecucion],ejecucion)"""		
		
		

def limpiar_memoria():
	i=0
	while (memory[i][1]!=ejecucion):
		i+=1
	memory[i][1]=0
	estado_memori=True
	if tipo_de_memoria in [3,4]:
		if (memory[i-1][1]==0) and (memory[i+1][1]==0):
			memory[i-1][0]=memory[i-1][0]+memory[i][0]+memory[i+1][0]
		elif (memory[i-1][1]==0):
			memory[i-1][0]=memory[i-1][0]+memory[i][0]
		elif (memory[i+1][1]==0):
			memory[i][0]=memory[i][0]+memory[i+1][0]

"""siempre termina con un de proceso teoria preguntar Ian"""
def fsfc(d):
	d[ejecucion][pos_data[ejecucion]]-=1
	if (d[ejecucion][pos_data[ejecucion]]==0):
		if (pos_data[ejecucion]==5):
			limpiar_memoria()
			d.pop(ejecucion)
			ejecucion= "-"
			return
		pos_data[ejecucion]+=1
		control_bloqueo(pos_data[ejecucion],ejecucion)
		ejecucion=cola_listo_proceso[1]

"""esta esta ocupando espacio"""
bubblemM(data)
tiempo=0
"""principal 1 ve si es mejor preguntar afiera del while cual proceso y memoria """
while len(data)!=0:
	cargar_cola_listo_memoria(cola_listo_memoria)
	pp_ff(memory)
	
	if(control_1):
		"""primero salida"""

	
		"""segundo Entrada"""


	"""tercero Proceso"""
	cargar_ejecucion()
	
	
		


	"""final"""
	tiempo+=1



"""recordar que cuando termina un roceso 
tenes que liverar la memoria =-1"""