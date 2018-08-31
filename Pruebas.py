import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QIcon


class Ventana(QWidget):

    def __init__(self):
        super().__init__()
        self.iniciarGUI()

    def iniciarGUI(self):
        self.setGeometry(300, 300, 300, 220)
        self.setWindowTitle('Simulador de Sistema Operativo')
        ##self.setWindowIcon(QIcon('web.png'))
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = Ventana()
    sys.exit(app.exec_())