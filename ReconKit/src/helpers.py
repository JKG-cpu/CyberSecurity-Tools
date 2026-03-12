import json
from os.path import join

class FileHandler:
    def __init__(self):
        # Filepaths from main.py
        self.results_fp = join("output", "results.json")

        self.results_data = self.load_data()
    
    def save_data(self, data: dict):
        if not isinstance(data, dict):
            print(f"Invalid data format: {type(data)}")
            return
        self.results_data.append(data)

        try:
            with open(self.results_fp, "w") as f:
                json.dump(self.results_data, f, indent = 4)
        
        except Exception as e:
            print(f"[X] Error saving data: {e}")

    def load_data(self) -> list:
        data = []

        try:
            with open(self.results_fp, "r") as f:
                data = json.load(f)
        
        except Exception as e:
            print(f"[X] Error loading data: {e}")
        
        return data