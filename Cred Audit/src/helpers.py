import json

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
                json.dump(data, f)
            
        except Exception as ex:
            print(f"Error saving data to {file_path}: {ex}")
            exit(1)
    