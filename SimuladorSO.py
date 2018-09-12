import sys
import mysql.connector
from mysql.connector import Error
from Form_CargaDeTrabajo import *
from Dialog_Importar import *
from Dialog_Guardar import *
from Dialog_Generar import *
from Dialog_Error import *
from Form_Memoria import *
from random import randint
from PyQt5.QtGui import QPainter, QColor, QFont


class VentanaCDT(Ui_Form_CargaDeTrabajo):
    def __init__(self):
        Ui_Form_CargaDeTrabajo.__init__(self)
        self.Form_CargaDeTrabajo = QtWidgets.QWidget()
        self.setupUi(self.Form_CargaDeTrabajo)
        self.eventos()
        self.ocultar_quantum()

    def eventos(self):
        self.lineEdit_NProcesos.textChanged.connect(self.mostrar_filas)
        self.radioButton_FCFS.clicked.connect(self.ocultar_quantum)
        self.radioButton_SJF.clicked.connect(self.ocultar_quantum)
        self.radioButton_SRTF.clicked.connect(self.ocultar_quantum)
        self.radioButton_ROUNDROBIN.clicked.connect(self.mostrar_quantum)
        self.pushButton_Importar.clicked.connect(self.ventana_importar)
        self.pushButton_Guardar.clicked.connect(self.ventana_guardar)
        self.pushButton_Generar.clicked.connect(self.ventana_generar)
        self.pushButton_Siguiente.clicked.connect(self.verificar_procesos)

    def obtener_nprocesos(self):
        if len(self.lineEdit_NProcesos.text()) > 0:
            nprocesos = int(self.lineEdit_NProcesos.text())
        else:
            nprocesos = 0
        return nprocesos

    def mostrar_filas(self):
        # CREAR FILAS
            nprocesos = self.obtener_nprocesos()
            self.tableWidget_Procesos.setRowCount(nprocesos)
        # ALINEAR CELDAS Y PONER TÍTULO A LAS FILAS
            for i in range(nprocesos):
                item = QtWidgets.QTableWidgetItem()
                self.tableWidget_Procesos.setVerticalHeaderItem(i, item)
                item.setText("P" + str(i + 1))
                for j in range(6):
                    item = QtWidgets.QTableWidgetItem()
                    item.setTextAlignment(QtCore.Qt.AlignCenter)
                    self.tableWidget_Procesos.setItem(i, j, item)

    def mostrar_quantum(self):
        self.label_Quantum.setVisible(True)
        self.lineEdit_Quantum.setVisible(True)

    def ocultar_quantum(self):
        self.label_Quantum.setVisible(False)
        self.lineEdit_Quantum.setVisible(False)

    @staticmethod
    def ventana_importar():
        ctrl.ventana_importar()

    @staticmethod
    def ventana_guardar():
        ctrl.ventana_guardar()

    @staticmethod
    def ventana_generar():
        ctrl.ventana_generar()

    def verificar_procesos(self):
        error_cpu = -1
        error_ta_vacio = -1
        error_ta_menor = -1
        ta_anterior = 0
        nprocesos = self.obtener_nprocesos()
        if nprocesos > 0:
            for i in range(nprocesos):
                if (self.tableWidget_Procesos.item(i, 0).text() == ""):
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
                ta_anterior = int(self.tableWidget_Procesos.item(i, 0).text())
            if error_cpu != -1:
                ctrl.uiError.error("Proceso P"+str(error_cpu)+": Todos los procesos deben iniciar y terminar con un ciclo de CPU.")
            elif error_ta_vacio != -1:
                ctrl.uiError.error("Proceso P"+str(error_ta_vacio)+": Se debe especificar el tiempo de arribo.")
            elif error_ta_menor != -1:
                ctrl.uiError.error("Proceso P"+str(error_ta_menor)+": El tiempo de arribo es menor al del proceso anterior.")
            else:
                self.Form_CargaDeTrabajo.close()
                ctrl.ventana_memoria(self.tableWidget_Procesos, nprocesos)
        else:
            ctrl.uiError.error("Debe existir al menos 1 proceso para ejecutar la simulación.")


class VentanaImportar(Ui_Dialog_Importar):
    def __init__(self):
        Ui_Dialog_Importar.__init__(self)
        self.Dialog_Importar = QtWidgets.QDialog()
        self.setupUi(self.Dialog_Importar)
        self.eventos()

    def eventos(self):
        self.pushButton_Cancelar.clicked.connect(self.Dialog_Importar.close)
        self.pushButton_Importar.clicked.connect(self.importar_cdt)

    def cargar_cdt(self):
        self.listWidget_CargasDeTrabajo.clear()
        qry = "SELECT nombre FROM CDT"
        cdt = ctrl.consultar(qry)
        for item in cdt:
            self.listWidget_CargasDeTrabajo.addItem(item[0])

    def importar_cdt(self):
        qry = "SELECT id, n_procesos FROM CDT WHERE nombre = '" + self.listWidget_CargasDeTrabajo.currentItem().text() + "'"
        resultado = ctrl.consultar(qry)[0]
        idcdt = resultado[0]
        nprocesos = resultado[1]
        ctrl.uiCDT.lineEdit_NProcesos.setText(str(nprocesos))
        qry = "SELECT tiempo_arribo, cpu1, entrada, cpu2, salida, cpu3 FROM Proceso WHERE id_cdt = " + str(idcdt)
        procesos = ctrl.consultar(qry)
        for i in range(len(procesos)):
            for j in range(6):
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

    def guardar_cdt(self):
        nombre = self.lineEdit_NombreCDT.text()
        nprocesos = ctrl.uiCDT.obtener_nprocesos()
        qry = "INSERT INTO CDT (nombre, n_procesos) VALUES (%s, %s)"
        valores = (nombre, nprocesos)
        ctrl.insertar(qry, valores)
        id = ctrl.consultar("SELECT LAST_INSERT_ID()")[0][0]
        qry = "INSERT INTO Proceso (id_cdt, id, tiempo_arribo, cpu1, entrada, cpu2, salida, cpu3)" \
              "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        for i in range(nprocesos):
            ta = int(ctrl.uiCDT.tableWidget_Procesos.item(i, 0).text())
            cpu1 = int(ctrl.uiCDT.tableWidget_Procesos.item(i, 1).text())
            e = int(ctrl.uiCDT.tableWidget_Procesos.item(i, 2).text())
            cpu2 = int(ctrl.uiCDT.tableWidget_Procesos.item(i, 3).text())
            s = int(ctrl.uiCDT.tableWidget_Procesos.item(i, 4).text())
            cpu3 = int(ctrl.uiCDT.tableWidget_Procesos.item(i, 5).text())
            valores = (id, i+1, ta, cpu1, e, cpu2, s, cpu3)
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

    def generar(self):
        nprocesos = ctrl.uiCDT.obtener_nprocesos()
        lim_inf = int(self.lineEdit_LimInf.text())
        lim_sup = int(self.lineEdit_LimSup.text())
        ta = 0
        ta_prom = round((lim_inf + lim_sup) * 2.5)
        if lim_sup <= lim_inf:
            ctrl.uiError.error("El límite superior debe ser mayor al límite inferior.")
        else:
            if lim_inf != 0:
                for i in range(nprocesos):
                    ctrl.uiCDT.tableWidget_Procesos.item(i, 0).setText(str(ta))
                    ta_lim_inf = ta
                    ta_lim_sup += ta + ta_prom
                    ta = randint(ta_lim_inf, ta_lim_sup)
                    for j in range(1, 6):
                        aleatorio = randint(lim_inf, lim_sup)
                        ctrl.uiCDT.tableWidget_Procesos.item(i, j).setText(str(aleatorio))
            else:
                for i in range(nprocesos):
                    # Tiempo de Arribo
                    ctrl.uiCDT.tableWidget_Procesos.item(i, 0).setText(str(ta))
                    ta_lim_inf = ta
                    ta_lim_sup = ta + ta_prom
                    ta = randint(ta_lim_inf, ta_lim_sup)
                    # CPU 1 debe ser mayor a 0
                    aleatorio = randint(1, lim_sup)
                    ctrl.uiCDT.tableWidget_Procesos.item(i, 1).setText(str(aleatorio))
                    # Entrada, CPU2 y Salida
                    for j in range(2, 5):
                        aleatorio = randint(lim_inf, lim_sup)
                        ctrl.uiCDT.tableWidget_Procesos.item(i, j).setText(str(aleatorio))
                    # CPU 3 debe ser mayor a 0
                    aleatorio = randint(1, lim_sup)
                    ctrl.uiCDT.tableWidget_Procesos.item(i, 5).setText(str(aleatorio))
        self.Dialog_Generar.close()


class VentanaError(Ui_Dialog_Error):
    def __init__(self):
        Ui_Dialog_Error.__init__(self)
        self.Dialog_Error = QtWidgets.QDialog()
        self.setupUi(self.Dialog_Error)
        self.eventos()

    def eventos(self):
        self.pushButton_Aceptar.clicked.connect(self.Dialog_Error.close)

    def error(self, descripcion):
        self.textBrowser_Error.setText("               ¡Error!\n" + descripcion)
        ctrl.ventana_error()


class VentanaMemoria(Ui_Form_Memoria):
    def __init__(self):
        Ui_Form_Memoria.__init__(self)
        self.Form_Memoria = QtWidgets.QWidget()
        self.setupUi(self.Form_Memoria)
        self.eventos()
        scene = QtWidgets.QGraphicsScene()
        self.graphicsView.setScene(scene)
        pen = QtGui.QPen(QtCore.Qt.green)

        side = 20

        for i in range(16):
            for j in range(16):
                r = QtCore.QRectF(QtCore.QPointF(i * side, j * side), QtCore.QSizeF(side, side))
                scene.addRect(r, pen)

    def eventos(self):
        self.pushButton_Atras.clicked.connect(self.ventana_cdt)

    @staticmethod
    def ventana_cdt():
        ctrl.ventana_cdt()


class Control:
    def __init__(self):
        self.uiCDT = VentanaCDT()
        self.uiImportar = VentanaImportar()
        self.uiGuardar = VentanaGuardar()
        self.uiGenerar = VentanaGenerar()
        self.uiError = VentanaError()
        self.uiMemoria = VentanaMemoria()

    def conectar_bd(self):
        try:
            self.bd = mysql.connector.connect(host='localhost', database='so', user='so', password='adminso')
        except Error as err:
            self.uiError.error("No se pudo conectar con la base de datos.\n"
                               "Las funciones Importar y Guardar estarán deshabilitadas.\n" + str(err))
            self.uiCDT.pushButton_Importar.setDisabled(True)
            self.uiCDT.pushButton_Guardar.setDisabled(True)

    def ventana_cdt(self):
        self.uiCDT.Form_CargaDeTrabajo.show()

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

    def ventana_memoria(self, procesos, nprocesos):
        self.uiMemoria.tableWidget_Procesos.setRowCount(nprocesos)
        for i in range(nprocesos):
            item = QtWidgets.QTableWidgetItem()
            self.uiMemoria.tableWidget_Procesos.setVerticalHeaderItem(i, item)
            item.setText("P" + str(i + 1))
            for j in range(6):
                item = QtWidgets.QTableWidgetItem()
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.uiMemoria.tableWidget_Procesos.setItem(i, j, item)
                item.setText(procesos.item(i, j).text())
                self.uiMemoria.tableWidget_Procesos.item(i, j).disabled()
        self.uiMemoria.Form_Memoria.show()

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

    # def importar_cdt(self):
    # if ctrl.uiCDT.radioButton_FCFS.isChecked():
    #     algoritmo = "FCFS"
    # elif ctrl.uiCDT.radioButton_SJF.isChecked():
    #     algoritmo = "SJF"
    # elif ctrl.uiCDT.radioButton_SRTF.isChecked():
    #     algoritmo = "SRTF"
    # elif ctrl.uiCDT.radioButton_ROUNDROBIN.isChecked():
    #     algoritmo = "ROUND ROBIN"