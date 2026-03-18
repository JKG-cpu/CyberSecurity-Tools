import hashlib
import os
import json
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from rich import print as rprint
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn
from os.path import join
from datetime import datetime

class FileIntegrityMonitor:
    def __init__(self):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))

        self.data_fp = join(BASE_DIR, "data", "data.json")
        self.changes_fp = join(BASE_DIR, "data", "changes.json")
        self.logs_dir = join(BASE_DIR, "logs")

        os.makedirs(join(BASE_DIR, "data"), exist_ok=True)

        self.data = self.load_data()
        self.changes = self.load_changes()

    # ── Data Saving + Loading ─────────────────────────────────────────────────
    def save_data(self, data: dict) -> None:
        try:
            with open(self.data_fp, "w") as f:
                json.dump(data, f, indent=4)

        except Exception as e:
            rprint(f"[red]Error saving data in {self.data_fp}: {e}[/red]")

    def load_data(self) -> dict:
        try:
            with open(self.data_fp, "r") as f:
                return json.load(f)

        except FileNotFoundError:
            return {}

        except json.JSONDecodeError as e:
            rprint(f"[red]Couldn't decode data file: {e}[/red]")
            return {}

    def save_changes(self, data: dict) -> None:
        try:
            with open(self.changes_fp, "w") as f:
                json.dump(data, f, indent=4)

        except Exception as e:
            rprint(f"[red]Error saving changes in {self.changes_fp}: {e}[/red]")

    def load_changes(self) -> dict:
        try:
            with open(self.changes_fp, "r") as f:
                return json.load(f)

        except FileNotFoundError:
            return {}

        except json.JSONDecodeError as e:
            rprint(f"[red]Couldn't decode changes file: {e}[/red]")
            return {}

    # ── Hashing ───────────────────────────────────────────────────────────────
    def hash_file(self, file_path: str) -> str | None:
        try:
            hasher = hashlib.sha256()
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(65536), b""):
                    hasher.update(chunk)
            return hasher.hexdigest()

        except (PermissionError, OSError):
            return None

    def hash_folder(self, folder_path: str) -> dict:
        data = {}

        # Collect all file paths first
        all_files = []
        for dirpath, _, filenames in os.walk(folder_path):
            for filename in filenames:
                all_files.append(join(dirpath, filename))

        # Hash in parallel with a progress bar
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("{task.completed}/{task.total} files"),
            TimeElapsedColumn(),
        ) as progress:
            task = progress.add_task("Scanning...", total=len(all_files))
            print()

            with ThreadPoolExecutor() as executor:
                futures = {executor.submit(self.hash_file, fp): fp for fp in all_files}
                for future in as_completed(futures):
                    fp = futures[future]
                    result = future.result()
                    if result:
                        data[fp] = result
                    progress.advance(task)

        return data

    # ── Logic ─────────────────────────────────────────────────────────────────
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

        for path in old_paths & new_paths:
            if data1[path] != data2[path]:
                changes["modified"].append(path)

        for path in new_paths - old_paths:
            changes["added"].append(path)

        for path in old_paths - new_paths:
            changes["deleted"].append(path)

        has_changes = any(changes.values())
        return (has_changes, changes)

    def save_log(self, changes: dict, timestamp: str) -> str:
        safe_timestamp = timestamp.replace(":", "-").replace(" ", "_")
        log_file = join(self.logs_dir, f"scan_{safe_timestamp}.txt")

        os.makedirs(self.logs_dir, exist_ok=True)

        with open(log_file, "w") as f:
            f.write(f"SCAN REPORT - {timestamp}\n")
            f.write("=" * 40 + "\n\n")

            for category in ["modified", "added", "deleted"]:
                files = changes[category]
                f.write(f"[{category.upper()}] — {len(files)} file(s)\n")
                for path in files:
                    f.write(f"  - {path}\n")
                f.write("\n")

        return os.path.abspath(log_file)

    def display_changes(self, changes: dict, timestamp: str) -> None:
        log_file = self.save_log(changes, timestamp)

        rprint(Panel.fit(f"Scan: {timestamp}", title="File Integrity Monitor", padding=(1, 10)))
        rprint()

        if not any(changes.values()):
            rprint("[green]✅  No changes detected[/green]\n")
            rprint(f"Log file: {log_file}\n")
            return

        rprint("⚠️  Changes detected!\n")

        if changes["modified"]:
            rprint(f"    🟡  Modified : {len(changes['modified'])} files")

        if changes["added"]:
            rprint(f"    🟢  Added    : {len(changes['added'])} files")

        if changes["deleted"]:
            rprint(f"    🔴  Deleted  : {len(changes['deleted'])} files")

        rprint(f"\nLog file: {log_file}\n")

    # ── Entry Point ───────────────────────────────────────────────────────────
    def scan(self, file_path: str) -> None:
        last_scan_data = self.data.get(file_path)
        timestamp = self.get_time()

        # Hash the target
        if os.path.isdir(file_path):
            data = self.hash_folder(file_path)
        else:
            data = {file_path: self.hash_file(file_path)}

        # First scan — create baseline
        if not last_scan_data:
            self.data[file_path] = data
            self.save_data(self.data)
            rprint(Panel.fit(f"Scan: {timestamp}", title="File Integrity Monitor", padding=(1, 10)))
            rprint("\n[blue]📁  Baseline created![/blue]")
            rprint(f"    Tracked [bold]{len(data)}[/bold] files\n")
            return

        # Compare against baseline
        _, changed_items = self.compare_data(last_scan_data, data)
        self.data[file_path] = data
        self.save_data(self.data)
        self.display_changes(changed_items, timestamp)

def main():
    parser = argparse.ArgumentParser(description="File Integrity Monitor")
    parser.add_argument("path", help="File or folder to scan")
    parser.add_argument("--desktop", action="store_true", help="Save log file to Desktop")
    parser.add_argument("--log-dir", type=str, help="Custom directory to save logs")
    args = parser.parse_args()

    path = os.path.abspath(os.path.expanduser(args.path))

    if not os.path.exists(path):
        rprint(f"[red]❌  Path not found: {path}[/red]")
        return

    fim = FileIntegrityMonitor()

    if args.desktop:
        fim.logs_dir = os.path.join(os.path.expanduser("~"), "Desktop")

    if args.log_dir:
        fim.logs_dir = os.path.abspath(args.log_dir)

    fim.scan(path)

if __name__ == "__main__":
    main()
