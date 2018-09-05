import sys
import mysql.connector
from mysql.connector import Error
from Form_CargaDeTrabajo import *
from Dialog_Importar import *


class VentanaPrincipal(Ui_Form_CargaDeTrabajo):
    def __init__(self):
        self.setupUi(Form_CargaDeTrabajo)
        self.eventos_de_usuario()
        Form_CargaDeTrabajo.show()

    def eventos_de_usuario(self):
        self.lineEdit_NProcesos.editingFinished.connect(self.mostrar_filas)
        self.pushButton_Guardar.clicked.connect(self.guardar_carga)
        self.pushButton_Importar.clicked.connect(self.importar_carga(Dialog_Importar))

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

    def conectar_bd(self):
        try:
            db = mysql.connector.connect(host='localhost', database='so', user='so', password='adminso')
            if db.is_connected():
                cursor = db.cursor()
                # cursor.execute("SELECT * FROM algoritmo")
                # resultado = cursor.fetchall()
                # cursor.close()
                # db.commit()
                # db.close()
                return db,cursor
        except Error as err:
            print("Error en la conexión a la base de datos: ", err)

    def guardar_carga(self):
        db, cursor = self.conectar_bd()
        filas = self.obtener_filas()
        qry = "INSERT INTO carga_de_trabajo (Nombre,N_procesos,Algoritmo) VALUES (%s,%s,%s)"
        valores = ("Prueba", filas, 1)
        cursor.execute(qry, valores)
        db.commit()

    def importar_carga(self,Dialog_Importar):
        Dialog_Importar.show()
        db, cursor = self.conectar_bd()
        filas = self.obtener_filas()
        qry = "SELECT carga_de_trabajo.Nombre, N_procesos, algoritmo.Nombre as Algoritmo FROM carga_de_trabajo INNER JOIN algoritmo ON carga_de_trabajo.Algoritmo=algoritmo.Id_algoritmo"
        cursor.execute(qry)
        resultado = cursor.fetchall()
        print(resultado)

class VentanaModal(Ui_Dialog_Importar):
    def __init__(self):
        self.setupUi(Dialog_Importar)
        Dialog_Importar.show()


class Control:
    def __init__(self):
        pass

    def Ventana():
        Form_CargaDeTrabajo = QtWidgets.QWidget()
        ui = VentanaPrincipal()

    def VentanaModal(self):
        Dialog_Importar = QtWidgets.QDialog()
        uiModal = Ui_Dialog_Importar()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    control=Control
    control.Ventana()

    sys.exit(app.exec_())