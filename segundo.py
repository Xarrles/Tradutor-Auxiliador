import win32gui
import win32con
import win32api
import pyautogui
import time

class Tradutor:
    def desenhar_retangulo(self, x, y, largura, altura, texto=None):
        """
        Desenha apenas o retângulo mais recente na tela do Windows usando GDI.
        Remove o desenho anterior ao criar um novo.
        """
        hwnd = win32gui.GetDesktopWindow()  # Janela da área de trabalho
        hdc = win32gui.GetDC(hwnd)         # Contexto de dispositivo

        try:
            # Cor e espessura do retângulo
            pen = win32gui.CreatePen(win32con.PS_SOLID, 2, win32api.RGB(0, 255, 0))
            brush = win32gui.GetStockObject(win32con.NULL_BRUSH)

            old_pen = win32gui.SelectObject(hdc, pen)
            old_brush = win32gui.SelectObject(hdc, brush)

            # Limpa a tela na área do retângulo anterior (invalida a área para ser redesenhada)
            win32gui.InvalidateRect(hwnd, None, True)

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
            # Restaurar os objetos antigos
            win32gui.SelectObject(hdc, old_pen)
            win32gui.SelectObject(hdc, old_brush)
            win32gui.ReleaseDC(hwnd, hdc)

# Loop para acompanhar o mouse e desenhar o retângulo
tradutor = Tradutor()

try:
    while True:
        # Posição do mouse e dimensões do retângulo
        x, y = pyautogui.position()
        largura = 500
        altura = 30

        # Atualizar o retângulo na posição do mouse
        tradutor.desenhar_retangulo(x - largura // 2, y - altura // 2, largura, altura, texto="Seguindo o mouse")
        time.sleep(0.1)  # Atualiza a cada 100ms

except KeyboardInterrupt:
    print("Encerrado pelo usuário.")
