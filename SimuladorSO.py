import sys
from VentanaPrincipal import *
import mysql.connector
from mysql.connector import Error

class Ventana(Ui_Form):
    def eventos_de_usuario(self):
        self.lineEdit_nprocesos.editingFinished.connect(self.mostrar_filas)
        self.pushButton_3.clicked.connect(self.guardar_carga)
        self.pushButton.clicked.connect(self.importar_carga)
    def obtener_filas(self):
        if len(self.lineEdit_nprocesos.text())>0:
            filas=int(self.lineEdit_nprocesos.text())
        else:
            filas=0
        return filas

    def mostrar_filas(self):
        #CREAR FILAS
            filas=self.obtener_filas()
            self.tableWidget.setRowCount(filas)
        #ALINEAR CELDAS Y PONER TITULO A LAS FILAS
            _translate = QtCore.QCoreApplication.translate
            for i in range(filas):
                item = QtWidgets.QTableWidgetItem()
                self.tableWidget.setVerticalHeaderItem(i, item)
                item.setText(_translate("Form", "P" + str(i + 1)))
                for j in range(6):
                    item = QtWidgets.QTableWidgetItem()
                    item.setTextAlignment(QtCore.Qt.AlignCenter)
                    self.tableWidget.setItem(i, j, item)

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

    def importar_carga(self):
        db, cursor = self.conectar_bd()
        filas = self.obtener_filas()
        qry = "SELECT carga_de_trabajo.Nombre, N_procesos, algoritmo.Nombre as Algoritmo FROM carga_de_trabajo INNER JOIN algoritmo ON carga_de_trabajo.Algoritmo=algoritmo.Id_algoritmo"
        cursor.execute(qry)
        resultado = cursor.fetchall()
        print(resultado)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ventana()
    ui.setupUi(Form)
    ui.eventos_de_usuario()
    Form.show()
    sys.exit(app.exec_())