import subprocess
import json
import argparse
from os.path import join

from src import *

class Main:
    def __init__(self) -> None:
        self.config_path = join("config", "config.json")
        self.results_path = join("output", "results.json")
        self.history_path = join("output", "history.json")

        self.filehander = FileHandler()

    def report(self) -> None:
        subprocess.run(
            ["dotnet", "run", "--project", "ReconProcessor", "--", "--report"],
            capture_output=True,
            text=True
        )

    def config(self) -> None:
        ui = UI()
        ui.main()

    def scan(self, report: bool = False) -> None:
        result = subprocess.run(
            ["dotnet", "run", "--project", "ReconProcessor", "--", "--config"],
            capture_output = True,
            text = True
        )

        if result.returncode != 0:
            print(f"Config validation failed: {result.stdout}")
            exit(1)

        with open(self.config_path) as f:
            config = json.load(f)
        
        NmapScanner(
            remote_host = config["remote_host"],
            start_port = config["start_port"],
            end_port = config["end_port"],
            max_concurrent = config["max_concurrent"]
        ).start_scan()

        try:
            history = self.filehander.load_path(self.history_path)
            history.append(self.filehander.load_path(self.results_path))
            self.filehander.save(self.history_path, history)

        except Exception as e:
            print(f"Error saving result history: {e}")

        if report:
            self.report()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "ReconKit")
    parser.add_argument("--report", action = "store_true", help = "Create a html file for the last scan result OR create a html file for the next scan (use with --scan)")
    parser.add_argument("--config", action = "store_true", help = "Config settings for the next scan.")
    parser.add_argument("--scan", action = "store_true", help = "Scan a host. Uses current config settings. Change with --config")
    args = parser.parse_args()

    if args.scan:
        Main().scan(args.report)

    elif args.config:
        Main().config()

    elif args.report:
        Main().report()

    else:
        parser.print_help()