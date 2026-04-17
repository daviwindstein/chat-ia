import pyautogui
import time
import os

def digitar_no_estudio(codigo):
    """Faz a IA esperar 5 segundos e digitar o script no editor aberto"""
    print("⚠️ Mude para a janela do Roblox Studio AGORA!")
    time.sleep(5)
    pyautogui.write(codigo, interval=0.001)
    print("✅ Script injetado!")

def criar_pasta_projeto(nome_projeto):
    """Cria uma pasta para o jogo no seu PC"""
    caminho = os.path.join(os.path.expanduser("~"), "Desktop", nome_projeto)
    if not os.path.exists(caminho):
        os.makedirs(caminho)
        return f"Pasta {nome_projeto} criada na Área de Trabalho!"
    return "A pasta já existe."
