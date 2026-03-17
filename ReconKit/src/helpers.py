import json
from os.path import join
from os import system, name

class FileHandler:
    def __init__(self):
        # Filepaths from main.py
        self.results_fp = join("output", "results.json")
    
    def load_path(self, file_path: str) -> dict | list:
        try:
            with open(file_path) as f:
                return json.load(f)

        except FileNotFoundError:
            print(f"File path: {file_path} could not be found.")
            exit(1)

    def save(self, file_path: str, data: dict | list) -> None:
        try:
            with open(file_path, "w") as f:
                json.dump(data, f, indent = 4)
        
        except FileNotFoundError:
            print(f"File path: {file_path} could not be found.")

def cc():
    system("cls" if name == "nt" else "clear")
    