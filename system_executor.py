import os

class SystemManager:
    def __init__(self):
        self.allow_pc_control = False

    def save_script(self, content, file_name, path):
        if not self.allow_pc_control:
            return "Erro: Permissão de acesso ao PC desativada."
        
        try:
            full_path = os.path.join(path, file_name)
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content)
            return f"Sucesso! Script salvo em: {full_path}"
        except Exception as e:
            return f"Erro ao salvar: {str(e)}"
