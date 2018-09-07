import sys
import mysql.connector
from mysql.connector import Error
from Form_CargaDeTrabajo import *
from Dialog_Importar import *
from Dialog_Guardar import *


class VentanaCDT(Ui_Form_CargaDeTrabajo):
    def __init__(self):
        Ui_Form_CargaDeTrabajo.__init__(self)
        self.Form_CargaDeTrabajo = QtWidgets.QWidget()
        self.setupUi(self.Form_CargaDeTrabajo)
        self.eventos()

    def eventos(self):
        self.lineEdit_NProcesos.editingFinished.connect(self.mostrar_filas)
        self.pushButton_Importar.clicked.connect(self.importar_carga)

    def obtener_filas(self):
        if len(self.lineEdit_NProcesos.text()) > 0:
            filas = int(self.lineEdit_NProcesos.text())
        else:
            filas = 0
        return filas

    def mostrar_filas(self):
        #CREAR FILAS
            filas = self.obtener_filas()
            self.tableWidget_Procesos.setRowCount(filas)
        #ALINEAR CELDAS Y PONER TITULO A LAS FILAS
            _translate = QtCore.QCoreApplication.translate
            for i in range(filas):
                item = QtWidgets.QTableWidgetItem()
                self.tableWidget_Procesos.setVerticalHeaderItem(i, item)
                item.setText(_translate("Form", "P" + str(i + 1)))
                for j in range(6):
                    item = QtWidgets.QTableWidgetItem()
                    item.setTextAlignment(QtCore.Qt.AlignCenter)
                    self.tableWidget_Procesos.setItem(i, j, item)

    def importar_carga(self):
        filas = self.obtener_filas()
        qry = "SELECT * FROM CDT"
        resultado = ctrl.consultar(qry)
        print(resultado)


class VentanaImportar(Ui_Dialog_Importar):
    def __init__(self):
        Ui_Dialog_Importar.__init__(self)
        self.Dialog_Importar = QtWidgets.QDialog()
        self.setupUi(self.Dialog_Importar)
        self.eventos()

    def eventos(self):
        self.pushButton_Cancelar.clicked.connect(self.Dialog_Importar.close)

    def cargar_cdt(self):
        self.listWidget_CargasDeTrabajo.clear()
        qry = "SELECT nombre_cdt FROM CDT"
        cargas = ctrl.consultar(qry)
        for i in cargas:
            aux = str(i)
            elemento = ''.join(j for j in aux if j.isalnum())
            self.listWidget_CargasDeTrabajo.addItem(elemento)

    # def importar_cdt(self):
        # if ctrl.uiCDT.radioButton_FCFS.isChecked():
        #     algoritmo = "FCFS"
        # elif ctrl.uiCDT.radioButton_SJF.isChecked():
        #     algoritmo = "SJF"
        # elif ctrl.uiCDT.radioButton_SRTF.isChecked():
        #     algoritmo = "SRTF"
        # elif ctrl.uiCDT.radioButton_ROUNDROBIN.isChecked():
        #     algoritmo = "ROUND ROBIN"


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
        nprocesos = ctrl.uiCDT.obtener_filas()
        qry = "INSERT INTO CDT (nombre_cdt, n_procesos) VALUES (%s,%s)"
        valores = (nombre, nprocesos)
        ctrl.insertar(qry, valores)
        self.Dialog_Guardar.close()

class Control:
    def __init__(self):
        try:
            self.bd = mysql.connector.connect(host='localhost', database='so', user='so', password='adminso')
        except Error as err:
            print("Error en la conexión a la base de datos: ", err)
        self.uiCDT = VentanaCDT()
        self.uiImportar = VentanaImportar()
        self.uiGuardar = VentanaGuardar()
        self.eventos()

    def ventana_cdt(self):
        self.uiCDT.Form_CargaDeTrabajo.show()

    def ventana_importar(self):
        self.uiImportar.Dialog_Importar.show()

    def ventana_guardar(self):
        self.uiGuardar.lineEdit_NombreCDT.clear()
        self.uiGuardar.Dialog_Guardar.show()

    def eventos(self):
        self.uiCDT.pushButton_Importar.clicked.connect(self.ventana_importar)
        self.uiCDT.pushButton_Importar.clicked.connect(self.uiImportar.cargar_cdt)
        self.uiCDT.pushButton_Guardar.clicked.connect(self.ventana_guardar)


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
    sys.exit(app.exec_())