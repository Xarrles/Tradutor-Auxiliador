import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor, QFont
from PyQt5.QtCore import Qt, QTimer, QThread, QRect
import pyautogui
from pytesseract import pytesseract
from googletrans import Translator
from PIL import Image
from io import BytesIO

pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'


class OCRThread(QThread):
    def __init__(self, screenshot, callback):
        super().__init__()
        self.screenshot = screenshot
        self.callback = callback

    def run(self):
        try:
            texto = pytesseract.image_to_string(self.screenshot)
            if texto.strip():
                tradutor = Translator()
                traducao = tradutor.translate(texto, dest="pt")
                self.callback(texto.strip(), traducao.text)
            else:
                self.callback("", "")
        except Exception as e:
            self.callback("", f"Erro: {e}")


class TransparentWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.start_pos = None
        self.end_pos = None
        self.is_selecting = False
        self.threads = []
        self.translated_text = ""
        self.font = QFont("Arial", 10)

    def initUI(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowOpacity(0.5)
        self.setGeometry(0, 0, pyautogui.size().width, pyautogui.size().height)

    def paintEvent(self, event):
        if self.start_pos and self.end_pos:
            painter = QPainter(self)
            pen = QPen(Qt.green, 3, Qt.SolidLine)
            painter.setPen(pen)

            # Desenhar o retângulo de seleção
            rect = QRect(self.start_pos, self.end_pos)
            painter.drawRect(rect)

            # Exibir texto traduzido, se disponível
            if self.translated_text:
                painter.setBrush(QBrush(QColor(250, 250, 250, 250)))
                painter.setPen(Qt.NoPen)
                painter.drawRect(rect.x(), rect.y() - 40, rect.width(), 30)

                painter.setPen(Qt.black)
                painter.setFont(self.font)
                painter.drawText(rect.x() + 5, rect.y() - 20, self.translated_text)

    def mousePressEvent(self, event):
        if QApplication.keyboardModifiers() == Qt.ControlModifier and event.button() == Qt.LeftButton:
            self.start_pos = event.pos()
            self.end_pos = None
            self.is_selecting = True

    def mouseMoveEvent(self, event):
        if self.is_selecting:
            self.end_pos = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.is_selecting:
            self.is_selecting = False
            self.end_pos = event.pos()
            self.capture_and_translate()

    def capture_and_translate(self):
        if self.start_pos and self.end_pos:
            x1 = min(self.start_pos.x(), self.end_pos.x())
            y1 = min(self.start_pos.y(), self.end_pos.y())
            x2 = max(self.start_pos.x(), self.end_pos.x())
            y2 = max(self.start_pos.y(), self.end_pos.y())

            region = (x1, y1, x2 - x1, y2 - y1)
            screenshot = pyautogui.screenshot(region=region)
            buffer = BytesIO()
            screenshot.save(buffer, format="PNG")
            self.process_ocr(buffer)

    def process_ocr(self, screenshot_buffer):
        def callback(texto, traducao):
            if texto:
                print(f"Texto capturado: {texto}")
                print(f"Tradução: {traducao}")
                self.translated_text = traducao
            else:
                self.translated_text = "Nenhum texto detectado."
            self.update()

        thread = OCRThread(Image.open(screenshot_buffer), callback)
        thread.finished.connect(lambda: self.cleanup_thread(thread))
        self.threads.append(thread)
        thread.start()

    def cleanup_thread(self, thread):
        self.threads.remove(thread)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TransparentWindow()
    window.show()
    sys.exit(app.exec_())
