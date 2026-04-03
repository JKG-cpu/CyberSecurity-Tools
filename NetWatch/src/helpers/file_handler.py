import json
from os.path import join

def get_config() -> dict:
    return FileHandler().load_data(join("config", "config.json"))

class FileHandler:
    def load_data(self, file_path: str) -> dict | list:
        try:
            with open(file_path, "r") as f:
                return json.load(f)
        
        except FileNotFoundError:
            print(f"Filepath {file_path} was not found")
        
        except Exception as e:
            print(f"Error loading data: {e}")
    
    def save(self, file_path: str, data: dict | list) -> None:
        try:
            with open(file_path, "w") as f:
                json.dump(data, f, indent = 4)
        
        except FileNotFoundError:
            print(f"Filepath {file_path} was not found")
        
        except Exception as e:
            print(f"Error saving data: {e}")
