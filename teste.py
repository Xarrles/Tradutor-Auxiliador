import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMouseEvent, QCursor
import pyautogui


import keyboard
import mouse

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.end_pos = None
        self.is_selecting = False
        self.setWindowTitle("Tecla CTRL e Mouse")
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowOpacity(0.5)
        self.setGeometry(0, 0, pyautogui.size().width, pyautogui.size().height)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)

    def mousePressEvent(self, event: QMouseEvent):
        if keyboard.is_pressed('ctrl') and  mouse.is_pressed('left'):
            print("Pressionou a tecla CTRL e o botão esquerdo do mouse")
            self.start_pos = QCursor.pos()
            print("Posição do mouse inicial: ", self.start_pos)
            self.end_pos = None
            self.is_selecting = True

        
    def mouseReleaseEvent(self, event: QMouseEvent):
        if not self.is_selecting:
            return
        if event.button() == Qt.LeftButton and QApplication.keyboardModifiers() == Qt.ControlModifier:
            print("Soltei a tecla CTRL e o botão esquerdo do mouse")
            self.end_pos = QCursor.pos()
            print("Posição do mouse final: ", self.end_pos)
            self.is_selecting = False

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())