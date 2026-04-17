import pyautogui
import time

print("🤖 ROBÔ DE AUTOMAÇÃO ATIVO")
print("Cole o script que a IA gerou aqui embaixo e dê ENTER:")
script = input("> ")

print("⚠️ Você tem 5 segundos para clicar no Roblox Studio...")
for i in range(5, 0, -1):
    print(f"{i}...")
    time.sleep(1)

pyautogui.write(script, interval=0.001)
print("✅ Concluído!")
