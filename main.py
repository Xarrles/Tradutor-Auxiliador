import pyautogui
from PIL import Image
import pytesseract
from googletrans import Translator
import win32gui
import win32con
import win32api
import time
from profilehooks import profile

pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

class Tradutor:

    def __init__(self):
        self.last_rect = None

    @profile
    def get_text(self):
        """
        Captura a tela na área definida pelo mouse, reconhece o texto e traduz.
        """
        try:
            # Posição do mouse e dimensões da área
            x, y = pyautogui.position()
            largura = 500
            altura = 30


            # Capturar a tela na região definida
            region = (x - largura // 2, y - altura // 2, largura, altura)
            self.desenhar_retangulo(x - largura // 2, y - altura // 2, largura, altura, texto="")


            screenshot = pyautogui.screenshot(region=region)
            screenshot.save("captura_temp.png")

            # Reconhecer texto
            texto = pytesseract.image_to_string(Image.open("captura_temp.png"))
            # Desenhar o retângulo antes de capturar

            # Traduzir texto, se detectado
            # if texto.strip():
            #     tradutor = Translator()
            #     traducao = tradutor.translate(texto, dest="pt")
            #     self.desenhar_retangulo(x - largura // 2, y - altura // 2, largura, altura, texto=traducao.text)
            #     print("Texto capturado:", texto)
            #     print("Tradução:", traducao.text)
            #     self.desenhar_retangulo(x - largura // 2, y - altura // 2, largura, altura, texto=traducao.text)
            # else:
            #     print("Nenhum texto detectado na região capturada.")

        except Exception as e:
            print(f"Erro: {e}")

    def desenhar_retangulo(self, x, y, largura, altura, texto=None):
        """
        Desenha apenas o retângulo mais recente na tela do Windows usando GDI.
        Remove o desenho anterior ao criar um novo.
        """
        hwnd = win32gui.GetDesktopWindow()
        hdc = win32gui.GetDC(hwnd)
        try:
        
            # Cor e espessura do retângulo
            pen = win32gui.CreatePen(win32con.PS_SOLID, 2, win32api.RGB(0, 255, 0))
            brush = win32gui.GetStockObject(win32con.NULL_BRUSH)
            old_pen = win32gui.SelectObject(hdc, pen)
            old_brush = win32gui.SelectObject(hdc, brush)

            # Desenhar o retângulo
            win32gui.Rectangle(hdc, x, y, x + largura, y + altura)

            # Exibir o texto (se fornecido)
            if texto:
                win32gui.SetTextColor(hdc, win32api.RGB(255, 255, 255))  # Cor do texto
                win32gui.SetBkMode(hdc, win32con.TRANSPARENT)  # Fundo transparente
                texto_pos_x = x
                texto_pos_y = y - 30  # Texto acima do retângulo
                win32gui.ExtTextOut(hdc, texto_pos_x, texto_pos_y, 0, None, texto, None)

        finally:
            # Restaurar objetos antigos
            win32gui.SelectObject(hdc, old_pen)
            win32gui.SelectObject(hdc, old_brush)
            win32gui.ReleaseDC(hwnd, hdc)




if __name__ == "__main__":
    print("Pressione Ctrl+C para sair.")
    tradutor = Tradutor()
    try:
        while True:
            print("Capturando texto na posição do mouse...")
            x, y = pyautogui.position()
            largura = 500
            altura = 30


            # Capturar a tela na região definida
            region = (x - largura // 2, y - altura // 2, largura, altura)
            tradutor.desenhar_retangulo(x - largura // 2, y - altura // 2, largura, altura, texto="")
    except KeyboardInterrupt:
        print("Programa encerrado.")