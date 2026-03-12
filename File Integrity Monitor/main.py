import hashlib
import os
import json
from rich import print as rprint
from rich.panel import Panel
from os.path import join
from datetime import datetime

def hash_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

class FileIntegrityMonitor:
    def __init__(self):
        self.data_fp = join("data", "data.json")
        self.changes_fp = join("data", "changes.json")

        self.data = self.load_data()
        self.changes = self.load_changes()

    # Data Saving + Loading
    #region
    def save_data(self, data: dict) -> None:
        try:
            with open(self.data_fp, "w") as f:
                json.dump(data, f, indent = 4)
        
        except Exception as e:
            print(f"Error saving data in {self.data_fp}: {e}")

    def load_data(self) -> dict:
        data = {}

        try:
            with open(self.data_fp, "r") as f:
                data = json.load(f)

        except FileNotFoundError as f:
            print(f"File not found error, can't load data: {f}.")
        
        except json.JSONDecodeError as e:
            print(f"Couldn't decode file, error: {e}")
        
        return data

    def save_changes(self, data: dict) -> None:
        try:
            with open(self.changes_fp, "w") as f:
                json.dump(data, f, indent = 4)
        
        except Exception as e:
            print(f"Error saving data in {self.changes_fp}: {e}")

    def load_changes(self) -> dict:
        changes = {}

        try:
            with open(self.changes_fp, "r") as f:
                changes = json.load(f)

        except FileNotFoundError as f:
            print(f"File not found error, can't load data: {f}.")
        
        except json.JSONDecodeError as e:
            print(f"Couldn't decode file, error: {e}")
        
        return changes
    #endregion

    # Files / Folders
    #region
    def hash_folder(self, folder_path: str) -> dict:
        data = {}

        for dirpath, _, filenames in os.walk(folder_path):
            for filename in filenames:
                full_path = join(dirpath, filename)
                
                hasher = hashlib.sha256()
                with open(full_path, "rb") as f:
                    for chunk in iter(lambda: f.read(65536), b""):
                        hasher.update(chunk)

                data[full_path] = hasher.hexdigest()
        
        return data

    def hash_file(self, file_path: str) -> str:
        hasher = hashlib.sha256()

        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                hasher.update(chunk)

        return hasher.hexdigest()
    #endregion

    # Logic
    def get_time(self) -> str:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def compare_data(self, data1: dict, data2: dict) -> tuple[bool, dict]:
        changes = {
            "modified": [],
            "added": [],
            "deleted": []
        }

        old_paths = set(data1.keys())
        new_paths = set(data2.keys())

        # Files that exist in both but hash changed
        for path in old_paths & new_paths:
            if data1[path] != data2[path]:
                changes["modified"].append(path)

        # Files that are new
        for path in new_paths - old_paths:
            changes["added"].append(path)

        # Files that were deleted
        for path in old_paths - new_paths:
            changes["deleted"].append(path)

        has_changes = any(changes.values())
        return (has_changes, changes)

    def save_log(self, changes: dict, timestamp: str) -> str:
        log_file = join("logs", f"scan_{timestamp.replace(":", "-").replace(" ", "_")}.txt")

        os.makedirs("logs", exist_ok = True)

        with open(log_file, "w") as f:
            f.write(f"SCAN REPORT - {timestamp}\n")
            f.write("=" * 40 + "\n\n")

            for category in ["modified", "added", "deleted"]:
                files = changes[category]
                f.write(f"[{category.upper()}] — {len(files)} file(s)\n")
                for path in files:
                    f.write(f"  - {path}\n")
                f.write("\n")
            
            f.write("\n\n")

        return log_file

    def display_changes(self, changes: dict, timestamp: str) -> None:
        log_file = self.save_log(changes, timestamp)
        log_file = os.path.abspath(log_file)
        
        rprint(Panel.fit(f"Scan: {timestamp}", title = "File Integrity Monitor", padding = (1, 10)))
        rprint()

        if not any(changes.values()):
            rprint("[green]✅  No changes detected[/green]\n")
            rprint(f"Log file path: {log_file}")
            rprint()
            return

        rprint("⚠️  Changes detected!")

        # Modified
        if changes["modified"]:
            rprint(f"    🟡  Modified : {len(changes["modified"])} files")

        # Added
        if changes["added"]:
            rprint(f"    🟢  Added : {len(changes["added"])} files")

        # Removed
        if changes["deleted"]:
            rprint(f"    🔴  Deleted : {len(changes["deleted"])} files")
        
        rprint(f"\nLog file path: {log_file}")
        rprint()

    # Entry Point
    def scan(self, file_path: str) -> None:
        data = {}
        last_scan_data = self.data.get(file_path)

        # Load data from new scan
        if os.path.isdir(file_path):
            data = self.hash_folder(file_path)
        
        else:
            data = self.hash_file(file_path)
            _, changed_items = self.compare_data(last_scan_data, data)
            self.display_changes(changed_items, timestamp)

        if last_scan_data:
            _, changed_items = self.compare_data(last_scan_data, data)
            self.data[file_path] = data

        else:
            self.data[file_path] = data

        # Save data
        self.save_data(self.data)

        # Save changes
        timestamp = self.get_time()
        self.display_changes(changed_items, timestamp)

if __name__ == "__main__":
    FileIntegrityMonitor().scan("C:/Users/FamilyPC/Desktop/Test Folder")