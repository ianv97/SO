import sys
from VentanaPrincipal import *





if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    ui.tableWidget.setRowCount(5)
    # item = self.tableWidget.verticalHeaderItem(0)
    # item.setText(_translate("Form", "P1"))
    Form.show()
    sys.exit(app.exec_())