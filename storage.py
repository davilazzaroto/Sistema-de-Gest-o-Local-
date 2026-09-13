#English - Exportation of important packages...
#Português - Exportação de pacotes importantes...
import json
import os

#English - Saving's Function...
#Português - Função de salvamento...
def save_json(data, file_path):
    with open(file_path, "w", encoding = "UTF-8", errors = "ignore") as f: 
        json.dump(data, f, ensure_ascii = False, indent = 4)

#English - Loading's Function
#Português - Função de carregamento...
def load_json(file_path):
    if not os.path.exists(file_path):
        return None
    with open(file_path, "r", encoding = "UTF-8", errors = "ignore") as f:
        return json.load(f)        