import sys
import mysql.connector
from mysql.connector import Error
from Form_CargaDeTrabajo import *
from Dialog_Importar import *


class VentanaPrincipal(Ui_Form_CargaDeTrabajo):
    def __init__(self):
        Ui_Form_CargaDeTrabajo.__init__(self)
        self.Form_CargaDeTrabajo = QtWidgets.QWidget()
        self.setupUi(self.Form_CargaDeTrabajo)
        self.eventos_de_usuario()
        self.Form_CargaDeTrabajo.show()

    def eventos_de_usuario(self):
        self.lineEdit_NProcesos.editingFinished.connect(self.mostrar_filas)
        self.pushButton_Guardar.clicked.connect(self.guardar_carga)
        self.pushButton_Importar.clicked.connect(self.importar_carga)
        self.pushButton_Importar.clicked.connect(uiModal.Dialog_Importar.show)

    def obtener_filas(self):
        if len(self.lineEdit_NProcesos.text())>0:
            filas=int(self.lineEdit_NProcesos.text())
        else:
            filas=0
        return filas

    def mostrar_filas(self):
        #CREAR FILAS
            filas=self.obtener_filas()
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


    def guardar_carga(self):
        filas = self.obtener_filas()
        qry = "INSERT INTO carga_de_trabajo (Nombre,N_procesos,Algoritmo) VALUES (%s,%s,%s)"
        valores = ("Prueba", filas, 1)
        bd.insertar(qry, valores)


    def importar_carga(self):
        filas = self.obtener_filas()
        qry = "SELECT carga_de_trabajo.Nombre, N_procesos, algoritmo.Nombre as Algoritmo FROM carga_de_trabajo INNER JOIN algoritmo ON carga_de_trabajo.Algoritmo=algoritmo.Id_algoritmo"
        resultado = bd.consultar(qry)
        print(resultado)

class db:
    def __init__(self):
        try:
            self.conector = mysql.connector.connect(host='localhost', database='so', user='so', password='adminso')
        except Error as err:
            print("Error en la conexión a la base de datos: ", err)

    def consultar(self,qry):
        cursor = self.conector.cursor()
        cursor.execute(qry)
        resultado = cursor.fetchall()
        cursor.close()
        return resultado

    def insertar(self,qry,valores):
        cursor = self.conector.cursor()
        resultado = cursor.execute(qry,valores)
        cursor.close()
        self.conector.commit()
        return resultado

class VentanaModal(Ui_Dialog_Importar):
    def __init__(self):
        Ui_Dialog_Importar.__init__(self)
        self.Dialog_Importar = QtWidgets.QDialog()
        self.setupUi(self.Dialog_Importar)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    bd=db()
    uiModal = VentanaModal()
    ui = VentanaPrincipal()

    sys.exit(app.exec_())