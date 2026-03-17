from rich import print as rprint
from rich.console import Console
from rich.panel import Panel
from os.path import join

from .helpers import cc, FileHandler

class UI:
    def __init__(self):
        self.running = True

        self.options = ["Remote Host", "Start Port", "End Port", "Max Concurrent", "Save and Exit"]
        self.console = Console()
        self.console.style = "bold white"

        self.config_path = join("config", "config.json")
        self.filehandler = FileHandler()
        self.data = self.filehandler.load_path(self.config_path)

    def display(self) -> None:
        rprint(Panel.fit("[italic]Config Settings[/]", title = "[italic]ReconKit[/]", padding = (1, 5)))
        rprint()

        # Current settings
        for item in ["remote_host", "start_port", "end_port", "max_concurrent"]:
            setting = self.data[item]
            rprint(f"[bold white]{item.replace("_", " ").title()}: {setting}")
        rprint()

        # Options
        for i, opt in enumerate(self.options, 1):
            rprint(f"[bold white]{i}. {opt}[/]")
        rprint()

    def main(self) -> None:
        while self.running:
            # Fresh Screen
            cc()
        
            self.display()

            user_input = self.console.input("Enter an option (number) > ")

            if user_input == "1":
                self.data["remote_host"] = self.console.input("Enter in the remote host > ")

            elif user_input == "2":
                try: 
                    self.data["start_port"] = int(self.console.input("Enter in the starting port > "))

                except:
                    self.console.input("Enter in a integer!")

            elif user_input == "3":
                try:
                    self.data["end_port"] = int(self.console.input("Enter in the ending port > "))

                except:
                    self.console.input("Enter in a integer!")

            elif user_input == "4":
                try:
                    self.data["max_concurrent"] = int(self.console.input("Enter in the max concurrency to use > "))

                except:
                    self.console.input("Enter in a integer!")

            elif user_input == "5":
                self.running = False

            else:
                pass

        self.filehandler.save(self.config_path, self.data)
