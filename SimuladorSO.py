import sys
from VentanaPrincipal import *

class Ventana(Ui_Form):
    def __init__(self):
        Ui_Form.__init__(self)

    def mostrarFilas(self):
        #CREAR FILAS
        if len(self.lineEdit_nprocesos.text())>0:
            filas=int(self.lineEdit_nprocesos.text())
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


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ventana()
    ui.setupUi(Form)
    ui.lineEdit_nprocesos.editingFinished.connect(ui.mostrarFilas)
    Form.show()
    sys.exit(app.exec_())