import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMouseEvent

class MainWindow(QMainWindow):
    def __init__(self):
        self.end_pos =  False
        self.is_selecting = False
        super().__init__()
        self.setWindowTitle("Tecla CTRL e Mouse")
        self.setGeometry(100, 100, 800, 600)\

    def mousePressEvent(self, event):
        if QApplication.keyboardModifiers() == Qt.ControlModifier and event.button() == Qt.LeftButton:
            print("Pressionou a tecla CTRL e o botão esquerdo do mouse")
            self.start_pos = event.pos()
            print("Posição do mouse inicial: ", self.start_pos)
            self.end_pos = None
            self.is_selecting = True

    def mouseReleaseEvent(self, event):
        if not self.is_selecting: return
        if not QApplication.keyboardModifiers() == Qt.ControlModifier or not event.button() == Qt.LeftButton:
            print("Soltei a tecla CTRL e o botão esquerdo do mouse")
            self.end_pos = event.pos()
            print("Posição do mouse final: ", self.end_pos)
            self.is_selecting = False

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
