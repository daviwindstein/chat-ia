import customtkinter as ctk
from brain_engine import GaiaEngine
from system_executor import SystemManager

class GaiaApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.engine = GaiaEngine()
        self.executor = SystemManager()

        # Configuração da Janela
        self.title("GAIA - AI Gamer & Dev")
        self.geometry("800x500")
        ctk.set_appearance_mode("dark")

        # UI - Barra de Pesquisa (Estilo Gemini)
        self.search_frame = ctk.CTkFrame(self, fg_color="#1e1f20", corner_radius=25)
        self.search_frame.pack(pady=50, padx=20, fill="x")

        self.entry = ctk.CTkEntry(self.search_frame, placeholder_text="Peça um script para Roblox ou Mine...", 
                                  border_width=0, fg_color="transparent", height=50)
        self.entry.pack(side="left", fill="x", expand=True, padx=20)

        self.btn_go = ctk.CTkButton(self.search_frame, text="⚡", width=50, corner_radius=25, command=self.run_ai)
        self.btn_go.pack(side="right", padx=10)

        # Switch de Permissão
        self.switch_var = ctk.StringVar(value="off")
        self.switch = ctk.CTkSwitch(self, text="Permitir que a IA mexa no meu PC", 
                                    command=self.toggle_permission, variable=self.switch_var, onvalue="on", offvalue="off")
        self.switch.pack(pady=10)

        self.output_text = ctk.CTkTextbox(self, height=200)
        self.output_text.pack(pady=20, padx=20, fill="both")

    def toggle_permission(self):
        self.executor.allow_pc_control = (self.switch_var.get() == "on")

    def run_ai(self):
        user_input = self.entry.get()
        # Exemplo: Se detectar 'Roblox', usa contexto Luau
        code = self.engine.generate_code(user_input)
        self.output_text.insert("0.0", f"--- CÓDIGO GERADO ---\n{code}\n")
        
        if self.executor.allow_pc_control:
            # Exemplo: Salvando na pasta do Rojo para Roblox
            res = self.executor.save_script(code, "GeneratedScript.lua", "./src")
            self.output_text.insert("0.0", f"{res}\n")

if __name__ == "__main__":
    app = GaiaApp()
    app.mainloop()
