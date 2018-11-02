import sys
import mysql.connector
from mysql.connector import Error
from Form_CargaDeTrabajo import *
from Dialog_Importar import *
from Dialog_Guardar import *
from Dialog_Generar import *
from Dialog_Error import *
from Dialog_Particion import *
from Form_Resultado import *
from random import randint
import plotly
import plotly.figure_factory as ff
from Algoritmos import *

def screen_size():
    if sys.platform == 'win32':
        import ctypes
        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware()
        return [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]
    else:
        import subprocess
        size = (None, None)
        args = ["xrandr", "-q", "-d", ":0"]
        proc = subprocess.Popen(args,stdout=subprocess.PIPE)
        for line in proc.stdout:
            if isinstance(line, bytes):
                line = line.decode("utf-8")
                if "Screen" in line:
                    size = (int(line.split()[7]),  int(line.split()[9][:-1]))
        return size

class VentanaCDT(Ui_Form_CargaDeTrabajo):
    def __init__(self):
        Ui_Form_CargaDeTrabajo.__init__(self)
        self.Form_CargaDeTrabajo = QtWidgets.QWidget()
        self.setupUi(self.Form_CargaDeTrabajo)
        self.Form_CargaDeTrabajo.setStyleSheet("background-image: url(Recursos/Fondo.jpg);")
        self.pushButton_CorrerSimulacion.setStyleSheet("background-image: url(Recursos/Fondo2.jpg); color: rgb(255,255,255);")
        self.tableWidget_Procesos.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.escena = QtWidgets.QGraphicsScene()
        self.pincel = QtGui.QPen(QtCore.Qt.yellow)
        self.pincel.setWidth(5)
        self.graphicsView.setScene(self.escena)
        self.escena_altura = self.escena.height()
        self.escena_fuente = QtGui.QFont()
        self.escena_fuente.setBold(True)
        self.escena_fuente.setPixelSize(20)
        self.tamano_particiones = 0
        self.eventos()

    def eventos(self):
        self.ocultar_quantum()
        self.mostrar_filas()
        self.spinBox_Tamano.setReadOnly(True)
        self.pushButton_AnadirPart.setVisible(False)
        self.radioButton_FirstFit.setVisible(False)
        self.radioButton_WorstFit.setVisible(False)
        self.radioButton_BestFit.setVisible(False)
        self.spinBox_NProcesos.valueChanged.connect(self.mostrar_filas)
        self.radioButton_FCFS.clicked.connect(self.ocultar_quantum)
        self.radioButton_SJF.clicked.connect(self.ocultar_quantum)
        self.radioButton_SRTF.clicked.connect(self.ocultar_quantum)
        self.radioButton_ROUNDROBIN.clicked.connect(self.mostrar_quantum)
        self.pushButton_Importar.clicked.connect(self.ventana_importar)
        self.pushButton_Guardar.clicked.connect(self.ventana_guardar)
        self.pushButton_Generar.clicked.connect(self.ventana_generar)
        self.pushButton_CorrerSimulacion.clicked.connect(self.correr_simulacion)
        self.radioButton_PartFijas.clicked.connect(self.desactivar_tamano)
        self.radioButton_PartFijas.clicked.connect(self.mostrar_boton_particion)
        self.radioButton_PartFijas.clicked.connect(self.reiniciar_asignacion)
        self.radioButton_PartFijas.clicked.connect(self.mostrar_algoritmos_pfijas)
        self.pushButton_AnadirPart.clicked.connect(self.ventana_particion)
        self.radioButton_PartVariables.clicked.connect(self.activar_tamano)
        self.radioButton_PartVariables.clicked.connect(self.ocultar_boton_particion)
        self.radioButton_PartVariables.clicked.connect(self.reiniciar_asignacion)
        self.radioButton_PartVariables.clicked.connect(self.mostrar_algoritmos_pvariables)
        self.spinBox_Tamano.valueChanged.connect(self.graficar_particiones_variables)
        self.pushButton_Cerrar.clicked.connect(self.Form_CargaDeTrabajo.close)
        self.pushButton_Minimizar.clicked.connect(self.Form_CargaDeTrabajo.showMinimized)
        self.pushButton_Ventana.clicked.connect(self.modo_ventana)

    def obtener_nprocesos(self):
        if len(self.spinBox_NProcesos.text()) > 0:
            nprocesos = int(self.spinBox_NProcesos.text())
        else:
            nprocesos = 0
        return nprocesos

    def mostrar_filas(self):
        # HABILITAR/DESHABILITAR GUARDAR Y GENERAR
        if self.spinBox_NProcesos.value() > 0:
            if ctrl.error_bd == 0:
                self.pushButton_Guardar.setEnabled(True)
                self.pushButton_Guardar.setStyleSheet("background-image:url(); background-color: rgb(0, 123, 255)")
            self.pushButton_Generar.setEnabled(True)
            self.pushButton_Generar.setStyleSheet("background-image:url(); background-color: rgb(0, 123, 255)")
        else:
            self.pushButton_Guardar.setDisabled(True)
            self.pushButton_Generar.setDisabled(True)
            self.pushButton_Guardar.setStyleSheet("background-image:url(); background-color: rgb(50, 50, 50)")
            self.pushButton_Generar.setStyleSheet("background-image:url(); background-color: rgb(50, 50, 50)")
        # CREAR FILAS
        nprocesos = self.obtener_nprocesos()
        self.tableWidget_Procesos.setRowCount(nprocesos)
        # ALINEAR CELDAS Y PONER TÍTULO A LAS FILAS
        for i in range(nprocesos):
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget_Procesos.setVerticalHeaderItem(i, item)
            item.setText("P" + str(i + 1))
            for j in range(7):
                item = QtWidgets.QTableWidgetItem()
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.tableWidget_Procesos.setItem(i, j, item)

    def mostrar_quantum(self):
        self.label_Quantum.setVisible(True)
        self.spinBox_Quantum.setVisible(True)

    def ocultar_quantum(self):
        self.label_Quantum.setVisible(False)
        self.spinBox_Quantum.setVisible(False)

    @staticmethod
    def ventana_importar():
        ctrl.ventana_importar()

    @staticmethod
    def ventana_guardar():
        ctrl.ventana_guardar()

    @staticmethod
    def ventana_generar():
        ctrl.ventana_generar()

    def graficar_particiones_fijas(self, tamano):
        rectangulo = QtCore.QRectF(QtCore.QPointF(0, self.tamano_particiones), QtCore.QSizeF(350, tamano*2))
        self.escena.addRect(rectangulo, self.pincel)
        texto = self.escena.addText(str(tamano)+' KB', self.escena_fuente)
        texto.setPos(135, self.tamano_particiones + tamano - 15)
        texto.setDefaultTextColor(QtGui.QColor(255, 255, 255, 255))
        self.tamano_particiones += tamano*2

    def graficar_particiones_variables(self):
        if self.radioButton_PartVariables.isChecked():
            self.escena.clear()
            tamano = int(self.spinBox_Tamano.text())
            rectangulo = QtCore.QRectF(QtCore.QPointF(0, 0), QtCore.QSizeF(350, tamano*2))
            self.escena.addRect(rectangulo, self.pincel)
            texto = self.escena.addText(str(tamano) + ' KB', self.escena_fuente)
            texto.setPos(135, tamano - 15)
            texto.setDefaultTextColor(QtGui.QColor(255, 255, 255, 255))

    @staticmethod
    def ventana_particion():
        ctrl.ventana_particion()

    def desactivar_tamano(self):
        self.spinBox_Tamano.setReadOnly(True)

    def activar_tamano(self):
        self.spinBox_Tamano.setReadOnly(False)

    def ocultar_boton_particion(self):
        self.pushButton_AnadirPart.setVisible(False)

    def mostrar_boton_particion(self):
        self.pushButton_AnadirPart.setVisible(True)

    def reiniciar_asignacion(self):
        global particiones
        particiones.clear()
        self.tamano_particiones = 0
        self.spinBox_Tamano.setValue(0)
        self.escena.clear()

    def mostrar_algoritmos_pfijas(self):
        self.radioButton_FirstFit.setVisible(True)
        self.radioButton_BestFit.setVisible(True)
        self.radioButton_WorstFit.setVisible(False)

    def mostrar_algoritmos_pvariables(self):
        self.radioButton_FirstFit.setVisible(True)
        self.radioButton_BestFit.setVisible(False)
        self.radioButton_WorstFit.setVisible(True)

    def correr_simulacion(self):
        global matriz_procesos
        matriz_procesos.clear()
        matriz_procesos.append([0, 99999999, 99999999, 99999999, 99999999, 99999999])
        global matriz_resultados
        matriz_resultados.clear()
        global cola_memoria
        cola_memoria.clear()
        global cola_listos
        cola_listos.clear()
        global cola_entrada
        cola_entrada.clear()
        global cola_salida
        cola_salida.clear()
        global lista_completados
        lista_completados.clear()

        error_cpu = -1
        error_ta_vacio = -1
        error_ta_menor = -1
        error_proceso_sin_memoria = -1
        error_memoria_insuficiente = -1
        error_particion_insuficiente = -1
        ta_anterior = 0
        nprocesos = self.obtener_nprocesos()
        if self.radioButton_PartVariables.isChecked():
            t_memoria = self.spinBox_Tamano.value()
            particiones.append([t_memoria, 0])
        elif len(particiones) > 0:
            t_memoria = 0
            for i in particiones:
                if i[0] > t_memoria:
                    t_memoria = i[0]
        else:
            t_memoria = 0
        if not self.radioButton_FCFS.isChecked() and not self.radioButton_SJF.isChecked() \
        and not self.radioButton_SRTF.isChecked() and not self.radioButton_ROUNDROBIN.isChecked():
            ctrl.uiError.error("Debe seleccionar un algoritmo.")
        elif self.radioButton_ROUNDROBIN.isChecked() and self.spinBox_Quantum.value()==0:
            ctrl.uiError.error("Debe ingresar un quantum mayor a 0.")
        elif not self.radioButton_PartFijas.isChecked() and not self.radioButton_PartVariables.isChecked():
            ctrl.uiError.error("Debe seleccionar un mecanismo de particiones.")
        elif (self.radioButton_PartFijas.isChecked() and not (self.radioButton_FirstFit.isChecked() or self.radioButton_BestFit.isChecked()))\
                or (self.radioButton_PartVariables.isChecked() and not (self.radioButton_FirstFit.isChecked() or self.radioButton_WorstFit.isChecked())):
            ctrl.uiError.error("Debe seleccionar un algoritmo de asignación de memoria.")
        else:
            if nprocesos > 0:
                for i in range(nprocesos):
                    if self.tableWidget_Procesos.item(i, 0).text() == "":
                        error_ta_vacio = i+1
                        break
                    elif (self.tableWidget_Procesos.item(i, 1).text() == "0") or \
                            (self.tableWidget_Procesos.item(i, 1).text() == "") or \
                            (self.tableWidget_Procesos.item(i, 5).text() == "0") or \
                            (self.tableWidget_Procesos.item(i, 5).text() == ""):
                        error_cpu = i+1
                        break
                    elif int(self.tableWidget_Procesos.item(i, 0).text()) < ta_anterior:
                        error_ta_menor = i+1
                        break
                    elif int(self.tableWidget_Procesos.item(i, 6).text()) == 0:
                        error_proceso_sin_memoria = i + 1
                        break
                    elif int(self.tableWidget_Procesos.item(i, 6).text()) > t_memoria:
                        if self.radioButton_PartVariables.isChecked():
                            error_memoria_insuficiente = i + 1
                        else:
                            error_particion_insuficiente = i + 1
                        break
                    ta_anterior = int(self.tableWidget_Procesos.item(i, 0).text())
                if error_cpu != -1:
                    ctrl.uiError.error("Proceso P"+str(error_cpu)+": Todos los procesos deben iniciar y terminar con un ciclo de CPU.")
                elif error_ta_vacio != -1:
                    ctrl.uiError.error("Proceso P"+str(error_ta_vacio)+": Se debe especificar el tiempo de arribo.")
                elif error_ta_menor != -1:
                    ctrl.uiError.error("Proceso P"+str(error_ta_menor)+": El tiempo de arribo es menor al del proceso anterior.")
                elif error_proceso_sin_memoria != -1:
                    ctrl.uiError.error("Proceso P" + str(error_proceso_sin_memoria) + ": La memoria requerida por el proceso no puede ser nula.")
                elif error_memoria_insuficiente != -1:
                    ctrl.uiError.error("Proceso P" + str(error_memoria_insuficiente) + ": La memoria total es insuficiente para este proceso.")
                elif error_particion_insuficiente != -1:
                    ctrl.uiError.error("Proceso P" + str(error_particion_insuficiente) + ": Ninguna partición posee el tamaño requerido por este proceso.")
                else:
                    for i in range(nprocesos):
                        matriz_procesos.append([])
                        for j in range(7):
                            matriz_procesos[i+1].append(int(self.tableWidget_Procesos.item(i, j).text()))

                    if ctrl.uiCDT.radioButton_PartFijas.isChecked():
                        part = 'FIJAS'
                        if ctrl.uiCDT.radioButton_FirstFit.isChecked():
                            alg_part = 'FF'
                        elif ctrl.uiCDT.radioButton_BestFit.isChecked():
                            alg_part = 'BF'
                    elif ctrl.uiCDT.radioButton_PartVariables.isChecked():
                        part = 'VARIABLES'
                        if ctrl.uiCDT.radioButton_FirstFit.isChecked():
                            alg_part = 'FF'
                        elif ctrl.uiCDT.radioButton_WorstFit.isChecked():
                            alg_part = 'WF'
                    if ctrl.uiCDT.radioButton_FCFS.isChecked():
                        no_apropiativos(part, alg_part, 'FCFS')
                    elif ctrl.uiCDT.radioButton_SJF.isChecked():
                        no_apropiativos(part, alg_part, 'SJF')
                    elif ctrl.uiCDT.radioButton_SRTF.isChecked():
                        apropiativos(part, alg_part, 'SRTF')
                    elif ctrl.uiCDT.radioButton_ROUNDROBIN.isChecked():
                        apropiativos(part, alg_part, 'RR', self.spinBox_Quantum.value())
                    ctrl.ventana_resultado()
            else:
                ctrl.uiError.error("Debe existir al menos 1 proceso para ejecutar la simulación.")

    def modo_ventana(self):
        if self.Form_CargaDeTrabajo.isFullScreen():
            self.pushButton_Minimizar.setHidden(True)
            self.pushButton_Cerrar.setHidden(True)
            self.Form_CargaDeTrabajo.showMaximized()
        else:
            self.pushButton_Minimizar.setHidden(False)
            self.pushButton_Cerrar.setHidden(False)
            self.Form_CargaDeTrabajo.showFullScreen()


class VentanaImportar(Ui_Dialog_Importar):
    def __init__(self):
        Ui_Dialog_Importar.__init__(self)
        self.Dialog_Importar = QtWidgets.QDialog()
        self.setupUi(self.Dialog_Importar)
        self.eventos()

    def eventos(self):
        self.pushButton_Cancelar.clicked.connect(self.Dialog_Importar.close)
        self.pushButton_Importar.clicked.connect(self.importar_cdt)
        self.listWidget_CargasDeTrabajo.doubleClicked.connect(self.importar_cdt)
        self.pushButton_Importar.setDefault(True)

    def cargar_cdt(self):
        self.listWidget_CargasDeTrabajo.clear()
        qry = "SELECT nombre FROM CDT"
        cdt = ctrl.consultar(qry)
        for item in cdt:
            self.listWidget_CargasDeTrabajo.addItem(item[0])

    def importar_cdt(self):
        qry = "SELECT id, n_procesos, t_memoria FROM CDT WHERE nombre = '" + self.listWidget_CargasDeTrabajo.currentItem().text() + "'"
        resultado = ctrl.consultar(qry)[0]
        ctrl.id_cdt = resultado[0]
        nprocesos = resultado[1]
        t_memoria = resultado[2]
        ctrl.uiCDT.spinBox_NProcesos.setValue(nprocesos)
        qry = "SELECT COUNT(*) FROM Particiones WHERE id_cdt = " + str(ctrl.id_cdt)
        n_particiones = ctrl.consultar(qry)[0][0]
        if n_particiones == 0:
            ctrl.uiCDT.radioButton_PartVariables.click()
        else:
            ctrl.uiCDT.radioButton_PartFijas.click()
            qry = "SELECT tamano FROM Particiones WHERE id_cdt = " + str(ctrl.id_cdt)
            resultado = ctrl.consultar(qry)
            for i in range(n_particiones):
                ctrl.uiParticion.agregar_particion(resultado[i][0])
        ctrl.uiCDT.spinBox_Tamano.setValue(t_memoria)
        qry = "SELECT tiempo_arribo, cpu1, entrada, cpu2, salida, cpu3, memoria FROM Proceso WHERE id_cdt = " + str(ctrl.id_cdt)
        procesos = ctrl.consultar(qry)
        for i in range(len(procesos)):
            for j in range(7):
                ctrl.uiCDT.tableWidget_Procesos.item(i, j).setText(str(procesos[i][j]))
        self.Dialog_Importar.close()


class VentanaGuardar(Ui_Dialog_Guardar):
    def __init__(self):
        Ui_Dialog_Guardar.__init__(self)
        self.Dialog_Guardar = QtWidgets.QDialog()
        self.setupUi(self.Dialog_Guardar)
        self.eventos()

    def eventos(self):
        self.pushButton_Cancelar.clicked.connect(self.Dialog_Guardar.close)
        self.pushButton_Guardar.clicked.connect(self.guardar_cdt)
        self.pushButton_Guardar.setDefault(True)

    def guardar_cdt(self):
        nombre = self.lineEdit_NombreCDT.text()
        nprocesos = ctrl.uiCDT.obtener_nprocesos()
        t_memoria = int(ctrl.uiCDT.spinBox_Tamano.text())
        qry = "INSERT INTO CDT (nombre, n_procesos, t_memoria) VALUES (%s, %s, %s)"
        valores = (nombre, nprocesos, t_memoria)
        ctrl.insertar(qry, valores)
        ctrl.id_cdt = ctrl.consultar("SELECT LAST_INSERT_ID()")[0][0]
        if ctrl.uiCDT.radioButton_PartFijas.isChecked():
            qry = "INSERT INTO Particiones (id_cdt, id, tamano) VALUES (%s, %s, %s)"
            for j in range(len(particiones)):
                valores = (ctrl.id_cdt, j, particiones[j][0])
                ctrl.insertar(qry, valores)
        qry = "INSERT INTO Proceso (id_cdt, id, tiempo_arribo, cpu1, entrada, cpu2, salida, cpu3, memoria)" \
              "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        for i in range(nprocesos):
            ta = int(ctrl.uiCDT.tableWidget_Procesos.item(i, 0).text())
            cpu1 = int(ctrl.uiCDT.tableWidget_Procesos.item(i, 1).text())
            e = int(ctrl.uiCDT.tableWidget_Procesos.item(i, 2).text())
            cpu2 = int(ctrl.uiCDT.tableWidget_Procesos.item(i, 3).text())
            s = int(ctrl.uiCDT.tableWidget_Procesos.item(i, 4).text())
            cpu3 = int(ctrl.uiCDT.tableWidget_Procesos.item(i, 5).text())
            memoria = int(ctrl.uiCDT.tableWidget_Procesos.item(i, 6).text())
            valores = (ctrl.id_cdt, i+1, ta, cpu1, e, cpu2, s, cpu3, memoria)
            ctrl.insertar(qry, valores)
        self.Dialog_Guardar.close()


class VentanaGenerar(Ui_Dialog_Generar):
    def __init__(self):
        Ui_Dialog_Generar.__init__(self)
        self.Dialog_Generar = QtWidgets.QDialog()
        self.setupUi(self.Dialog_Generar)
        self.eventos()

    def eventos(self):
        self.pushButton_Cancelar.clicked.connect(self.Dialog_Generar.close)
        self.pushButton_Generar.clicked.connect(self.generar)
        self.pushButton_Generar.setDefault(True)

    def generar(self):
        nprocesos = ctrl.uiCDT.obtener_nprocesos()
        lim_inf = int(self.spinBox_LimInf.text())
        lim_sup = int(self.spinBox_LimSup.text())
        ta = 0
        t_memoria = 0
        if lim_sup == 0:
            ctrl.uiError.error("El límite superior debe ser mayor a 0.")
        elif lim_sup < lim_inf:
            ctrl.uiError.error("El límite superior debe ser mayor o igual al límite inferior.")
        else:
            if lim_inf != 0:
                for i in range(nprocesos):
                    ctrl.uiCDT.tableWidget_Procesos.item(i, 0).setText(str(ta))
                    ta_lim_inf = ta + (lim_inf * 5)
                    ta_lim_sup = ta + (lim_sup * 5)
                    ta = randint(ta_lim_inf, ta_lim_sup)
                    for j in range(1, 6):
                        aleatorio = randint(lim_inf, lim_sup)
                        ctrl.uiCDT.tableWidget_Procesos.item(i, j).setText(str(aleatorio))
            else:
                for i in range(nprocesos):
                    memoria = 0
                    # Tiempo de Arribo
                    ctrl.uiCDT.tableWidget_Procesos.item(i, 0).setText(str(ta))
                    ta_lim_inf = ta + (lim_inf * 5)
                    ta_lim_sup = ta + (lim_sup * 5)
                    ta = randint(ta_lim_inf, ta_lim_sup)
                    # CPU 1 debe ser mayor a 0
                    aleatorio = randint(1, lim_sup)
                    ctrl.uiCDT.tableWidget_Procesos.item(i, 1).setText(str(aleatorio))
                    memoria += aleatorio
                    # Entrada, CPU2 y Salida
                    for j in range(2, 5):
                        aleatorio = randint(lim_inf, lim_sup)
                        ctrl.uiCDT.tableWidget_Procesos.item(i, j).setText(str(aleatorio))
                        memoria += aleatorio
                    # CPU 3 debe ser mayor a 0
                    aleatorio = randint(1, lim_sup)
                    ctrl.uiCDT.tableWidget_Procesos.item(i, 5).setText(str(aleatorio))
                    memoria += aleatorio
                    # Memoria
                    ctrl.uiCDT.tableWidget_Procesos.item(i,6).setText(str(memoria * 3))
        self.Dialog_Generar.close()


class VentanaError(Ui_Dialog_Error):
    def __init__(self):
        Ui_Dialog_Error.__init__(self)
        self.Dialog_Error = QtWidgets.QDialog()
        self.setupUi(self.Dialog_Error)
        self.eventos()

    def eventos(self):
        self.pushButton_Aceptar.clicked.connect(self.Dialog_Error.close)
        self.pushButton_Aceptar.setDefault(True)

    def error(self, descripcion):
        self.textBrowser_Error.setText("               ¡Error!\n" + descripcion)
        ctrl.ventana_error()


class VentanaParticion(Ui_Dialog_Particion):
    def __init__(self):
        Ui_Dialog_Particion.__init__(self)
        self.Dialog_Particion = QtWidgets.QDialog()
        self.setupUi(self.Dialog_Particion)
        self.pushButton_Aceptar.setDefault(True)
        self.eventos()

    def eventos(self):
        self.pushButton_Aceptar.clicked.connect(self.agregar_particion)
        self.pushButton_Cancelar.clicked.connect(self.Dialog_Particion.close)

    def agregar_particion(self, tamano_nueva_particion=0):
        error = False
        if tamano_nueva_particion == 0:
            tamano_nueva_particion = int(self.spinBox_TamanoParticion.text())
            if tamano_nueva_particion == 0:
                ctrl.uiError.error("Debe asignar un tamaño mayor a 0 a la partición.")
                error = True
        if not error:
            ctrl.uiCDT.spinBox_Tamano.setValue(ctrl.uiCDT.tamano_particiones + tamano_nueva_particion)
            particiones.append([tamano_nueva_particion, 0])
            ctrl.uiCDT.graficar_particiones_fijas(tamano_nueva_particion)
            self.Dialog_Particion.close()


class VentanaResultado(Ui_Form_Resultado):
    def __init__(self):
        Ui_Form_Resultado.__init__(self)
        self.Form_Resultado = QtWidgets.QWidget()
        self.setupUi(self.Form_Resultado)
        self.tableWidget_Procesos.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.splitter.setSizes([0.75 * self.Form_Resultado.size().height(), 0.25 * self.Form_Resultado.size().height()])
        self.Form_Resultado.setStyleSheet("background-image: url(Recursos/Fondo.jpg);")
        self.eventos()

    def eventos(self):
        self.pushButton_Cerrar.clicked.connect(self.Form_Resultado.close)
        self.pushButton_Minimizar.clicked.connect(self.Form_Resultado.showMinimized)
        self.pushButton_Ventana.clicked.connect(self.modo_ventana)

    def formatear_tiempos(self, cadena):
        for i in range(4-len(cadena)):
            cadena = '0' + cadena
        return cadena

    def cargar(self):
        self.tableWidget_Procesos.setRowCount(len(matriz_resultados))
        procesos = []
        cpu = ''
        finish_cpu = 0
        entrada = ''
        finish_entrada = 0
        salida = ''
        finish_salida = 0
        for i in range(len(matriz_resultados)):
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget_Procesos.setVerticalHeaderItem(i, item)
            for j in range(10):
                item = QtWidgets.QTableWidgetItem()
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.tableWidget_Procesos.setItem(i, j, item)
                self.tableWidget_Procesos.item(i, j).setText(matriz_resultados[i][j])

            if cpu != matriz_resultados[i][7]:
                if cpu != '':
                    procesos.append(dict(Task="Proceso "+cpu, Start=self.formatear_tiempos(start_cpu), Finish=self.formatear_tiempos(str(finish_cpu)), Resource='CPU'))
                cpu = matriz_resultados[i][7]
                start_cpu = matriz_resultados[i][0]
                finish_cpu = int(start_cpu) + 1
            else:
                finish_cpu += 1

            if entrada != matriz_resultados[i][8]:
                if entrada != '':
                    procesos.append(dict(Task="Proceso "+entrada, Start=self.formatear_tiempos(start_entrada), Finish=self.formatear_tiempos(str(finish_entrada)), Resource='Entrada'))
                entrada = matriz_resultados[i][8]
                start_entrada = matriz_resultados[i][0]
                finish_entrada = int(start_entrada) + 1
            else:
                finish_entrada += 1

            if salida != matriz_resultados[i][9]:
                if salida != '':
                    procesos.append(dict(Task="Proceso "+salida, Start=self.formatear_tiempos(start_salida), Finish=self.formatear_tiempos(str(finish_salida)), Resource='Salida'))
                salida = matriz_resultados[i][9]
                start_salida = matriz_resultados[i][0]
                finish_salida = int(start_salida) + 1
            else:
                finish_salida += 1

        if cpu != '':
            procesos.append(dict(Task="Proceso " + cpu, Start=self.formatear_tiempos(start_cpu), Finish=self.formatear_tiempos(str(finish_cpu)), Resource='CPU'))
        if entrada != '':
            procesos.append(dict(Task="Proceso " + entrada, Start=self.formatear_tiempos(start_entrada), Finish=self.formatear_tiempos(str(finish_entrada)), Resource='Entrada'))
        if salida != '':
            procesos.append(dict(Task="Proceso " + salida, Start=self.formatear_tiempos(start_salida), Finish=self.formatear_tiempos(str(finish_salida)), Resource='Salida'))

        colores = {'CPU': 'rgb(220, 0, 0)',
                   'Entrada': (1, 0.9, 0.16),
                   'Salida': 'rgb(0, 123, 255)'}

        diagrama = ff.create_gantt(procesos, colors=colores, index_col='Resource', show_colorbar=True, group_tasks=True,
                                   title="Diagrama de Gantt", width=screen_size()[0] * 0.95,
                                   height=screen_size()[1] * 0.90, data=None)
        plotly.offline.plot(diagrama, auto_open=False)
        self.navegador.setUrl(QtCore.QUrl.fromLocalFile('/temp-plot.html'))


        self.navegador.loadFinished.connect(self.carga_completa)

    def carga_completa(self):
        ctrl.uiCDT.Form_CargaDeTrabajo.showMinimized()
        self.Form_Resultado.showFullScreen()

    def modo_ventana(self):
        if self.Form_Resultado.isFullScreen():
            self.pushButton_Minimizar.setHidden(True)
            self.pushButton_Cerrar.setHidden(True)
            self.Form_Resultado.showMaximized()
        else:
            self.pushButton_Minimizar.setHidden(False)
            self.pushButton_Cerrar.setHidden(False)
            self.Form_Resultado.showFullScreen()

class Control:
    def __init__(self):
        self.uiCDT = VentanaCDT()
        self.uiImportar = VentanaImportar()
        self.uiGuardar = VentanaGuardar()
        self.uiGenerar = VentanaGenerar()
        self.uiError = VentanaError()
        self.uiParticion = VentanaParticion()
        self.uiResultado = VentanaResultado()
        self.id_cdt = 0
        self.error_bd = 0

    def conectar_bd(self):
        archivo = open('DB.txt', 'r')
        host = archivo.readline()[6:-2]
        port = int(archivo.readline()[5:])
        database = archivo.readline()[10:-2]
        user = archivo.readline()[6:-2]
        password = archivo.readline()[10:-2]
        try:
            self.bd = mysql.connector.connect(host=host, port=port, database=database, user=user, password=password)
        except Error as err:
            self.uiError.error("No se pudo conectar con la base de datos.\n"
                               "Las funciones Importar y Guardar estarán deshabilitadas.\n" + str(err))
            self.error_bd = 1
            self.uiCDT.pushButton_Importar.setDisabled(True)
            self.uiCDT.pushButton_Guardar.setDisabled(True)
            self.uiCDT.pushButton_Importar.setStyleSheet("background-image:url(); background-color: rgb(50,50,50)")
            self.uiCDT.pushButton_Guardar.setStyleSheet("background-image:url(); background-color: rgb(50,50,50)")

    def ventana_cdt(self):
        self.uiCDT.Form_CargaDeTrabajo.showFullScreen()

    def ventana_importar(self):
        self.uiImportar.Dialog_Importar.show()
        self.uiImportar.cargar_cdt()

    def ventana_guardar(self):
        self.uiGuardar.lineEdit_NombreCDT.clear()
        self.uiGuardar.Dialog_Guardar.show()

    def ventana_generar(self):
        self.uiGenerar.Dialog_Generar.show()

    def ventana_error(self):
        self.uiError.Dialog_Error.show()

    def ventana_particion(self):
        self.uiParticion.Dialog_Particion.show()

    def ventana_resultado(self):
        self.uiResultado.cargar()

    def consultar(self, qry):
        cursor = self.bd.cursor()
        cursor.execute(qry)
        resultado = cursor.fetchall()
        cursor.close()
        return resultado

    def insertar(self, qry, valores):
        cursor = self.bd.cursor()
        resultado = cursor.execute(qry, valores)
        cursor.close()
        self.bd.commit()
        return resultado


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ctrl = Control()
    ctrl.ventana_cdt()
    ctrl.conectar_bd()
    sys.exit(app.exec_())