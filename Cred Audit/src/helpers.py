import json
from os.path import join

class FileLoader:
    def load(self, file_path: str) -> dict | list:
        try:
            with open(file_path, "r") as f:
                return json.load(f)
        
        except FileNotFoundError:
            print(f"File {file_path} not found")
            exit(1)
        
    def save(self, file_path: str, data: dict | list) -> None:
        try:
            with open(file_path, "w") as f:
                json.dump(data, f, indent = 4)
            
        except Exception as ex:
            print(f"Error saving data to {file_path}: {ex}")
            exit(1)
    
    def append_to_history(self, data) -> None:
        loaded_data = []

        with open(join("history", "history.json"), "r") as f:
            loaded_data = json.load(f)
        
        loaded_data.append(data)

        with open(join("history", "history.json"), "w") as f:
            json.dump(loaded_data, f, indent = 4)
            