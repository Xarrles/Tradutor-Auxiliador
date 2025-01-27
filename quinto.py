import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor, QFont, QFontMetrics
from PyQt5.QtCore import Qt, QTimer, QThread
import pyautogui
from pytesseract import pytesseract
from googletrans import Translator
from PIL import Image
from io import BytesIO
import keyboard
from time import sleep


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
        self.area_width = 300  # Largura inicial da área de captura
        self.area_height = 30  # Altura inicial da área de captura
        self.capture_active = True  # Estado inicial do fluxo de captura

    def initUI(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowOpacity(1.0)
        self.setGeometry(0, 0, pyautogui.size().width, pyautogui.size().height)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(100)  # Atualiza a cada 100ms
        self.mouse_pos = (0, 0)

    def keyPressEvent(self):
        """Captura eventos de teclado para ajustes de área e ativação/desativação do fluxo."""
        if keyboard.is_pressed('t'):  # Tecla 'T' para ativar/desativar
            self.capture_active = not self.capture_active
            print(f"Fluxo de captura {'ativado' if self.capture_active else 'desativado'}")

        elif (keyboard.is_pressed('w') or keyboard.is_pressed('up')):  # Ajustar altura
            while keyboard.is_pressed('w') or keyboard.is_pressed('up'):
                self.area_height += 10
                sleep(0.1)

        elif (keyboard.is_pressed('s') or keyboard.is_pressed('down')):  # Reduzir altura
            while keyboard.is_pressed('s') or keyboard.is_pressed('down'):
                self.area_height = max(10, self.area_height - 10)
                sleep(0.1)

        elif (keyboard.is_pressed('d') or keyboard.is_pressed('right')):  # Ajustar largura
            while keyboard.is_pressed('d') or keyboard.is_pressed('right'):
                self.area_width += 10
                sleep(0.1)

        elif (keyboard.is_pressed('a') or keyboard.is_pressed('left')):  # Reduzir largura
            while keyboard.is_pressed('a') or keyboard.is_pressed('left'):
                self.area_width = max(10, self.area_width - 10)
                sleep(0.1)

    def paintEvent(self, event):
        painter = QPainter(self)
        pen = QPen(Qt.green, 3, Qt.SolidLine)
        painter.setPen(pen)
        self.mouse_pos = pyautogui.position()
        self.keyPressEvent()  # Captura as teclas pressionadas
        largura, altura = self.area_width, self.area_height
        x, y = self.mouse_pos
        x -= largura // 2
        y -= altura // 2

        if not self.capture_active:
            x, y, largura, altura = 0, 0, 0, 0

        # Desenhar retângulo da área de captura
        painter.drawRect(x, y, largura, altura)

        # Verificar se o fluxo está ativo
        if self.capture_active and self.translated_text:
            text_x = x
            text_y = y - 10
            text_width = largura
            font_metrics = QFontMetrics(self.font)
            text_height = font_metrics.boundingRect(0, 0, text_width, 0, Qt.TextWordWrap, self.translated_text).height()

            # Fundo opaco
            painter.setBrush(QBrush(QColor(250, 250, 250, 250)))
            painter.setPen(Qt.NoPen)
            painter.drawRect(text_x, text_y - text_height, text_width, text_height)

            # Desenhar texto
            painter.setPen(Qt.black)
            painter.setFont(self.font)
            painter.drawText(text_x + 5, text_y - text_height, text_width - 10, text_height, Qt.TextWordWrap, self.translated_text)

        # Se o fluxo está ativo, realizar a captura e OCR
        if self.capture_active and self.mouse_pos != self.position_mouse:
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
                self.translated_text = traducao
            else:
                self.translated_text = "Nenhum texto detectado."

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
