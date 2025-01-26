import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor, QFont
from PyQt5.QtCore import Qt, QTimer, QThread
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
        self.position_mouse = None
        self.threads = []  # Lista para armazenar threads ativas
        self.translated_text = ""  # Texto traduzido para exibir na tela
        self.font = QFont("Arial", 10)  # Fonte do texto traduzido

    def initUI(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowOpacity(0.5)
        self.setGeometry(0, 0, pyautogui.size().width, pyautogui.size().height)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(100)  # Atualiza a cada 300ms
        self.mouse_pos = (0, 0)

    def paintEvent(self, event):
        painter = QPainter(self)
        pen = QPen(Qt.green, 3, Qt.SolidLine)
        painter.setPen(pen)
        self.mouse_pos = pyautogui.position()
        x, y = self.mouse_pos
        largura, altura = 680, 30
        x -= largura // 2
        y -= altura // 2
        painter.drawRect(x, y, largura, altura)

        # Desenhar fundo opaco para o texto traduzido
        if self.translated_text:
            text_x = x
            text_y = y - 40  # Acima do retângulo
            text_width = largura
            text_height = 30

            # Fundo opaco
            painter.setBrush(QBrush(QColor(250, 250, 250, 250)))  # Fundo preto com transparência
            painter.setPen(Qt.NoPen)  # Sem borda
            painter.drawRect(text_x, text_y, text_width, text_height)

            # Desenhar texto
            painter.setPen(Qt.black)  # Texto branco
            painter.setFont(self.font)
            painter.drawText(text_x + 5, text_y + 20, self.translated_text)

        if self.mouse_pos != self.position_mouse:
            self.position_mouse = self.mouse_pos
            region = (x, y, largura, altura)
            screenshot = pyautogui.screenshot(region=region)
            buffer = BytesIO()
            screenshot.save(buffer, format="PNG")
            self.process_ocr(buffer)

    def process_ocr(self, screenshot_buffer):
        def callback(texto, traducao):
            if texto:
                print(f"Texto capturado: {texto}")
                print(f"Tradução: {traducao}")
                self.translated_text = traducao  # Atualizar texto traduzido
            else:
                self.translated_text = "Nenhum texto detectado."

        # Criar e gerenciar thread
        thread = OCRThread(Image.open(screenshot_buffer), callback)
        thread.finished.connect(lambda: self.cleanup_thread(thread))
        self.threads.append(thread)
        thread.start()

    def cleanup_thread(self, thread):
        """Remove threads concluídas da lista."""
        self.threads.remove(thread)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TransparentWindow()
    window.show()
    sys.exit(app.exec_())