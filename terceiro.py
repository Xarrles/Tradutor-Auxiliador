import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QMouseEvent, QKeyEvent

import pyautogui


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tecla CTRL e Mouse")
        self.setGeometry(100, 100, 800, 600)


    def mousePressEvent(self, event: QMouseEvent):
        # Verifica se o botão esquerdo do mouse foi clicado
        if event.button() == Qt.LeftButton:
            print("Botão esquerdo do mouse pressionado.")

            # Verifica se a tecla CTRL está sendo pressionada
            if QApplication.keyboardModifiers() == Qt.ControlModifier:
                print("Tecla CTRL está pressionada.")
                self.start_pos = event.pos()
                print("Posição inicial: ", self.start_pos)

    def keyPressEvent(self, event: QKeyEvent):
        # Detecta se a tecla CTRL está pressionada
        if event.key() == Qt.Key_Control:
            print("Tecla CTRL detectada.")

    def keyReleaseEvent(self, event: QKeyEvent):
        # Detecta se a tecla CTRL foi liberada
        if event.key() == Qt.Key_Control:
            print("Tecla CTRL liberada.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
