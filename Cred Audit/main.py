import argparse
from rich import print
from rich.panel import Panel
from os.path import join
from os import system, name

from src import *

def cc():
    system("cls" if name == "nt" else "clear")

class CredAudit:
    def __init__(self):
        self.file_loader = FileLoader()
        self.hash_engine = HashingEngine()

        self.config_path = join("config", "config.json")
        self.config = self.file_loader.load(self.config_path)

    # Commands
    def config_settings(self) -> None:
        running = True

        while running:
            cc()

            print(Panel.fit("[italic bold white]Config Settings[/]", title = "[italic bold white]Cred Audit[/]", padding = (1, 5)))
            print()

            print("[bold white]1. Hash Type")
            print("[bold white]2. Word List Path")
            print("[bold white]3. Exit")
            print()

            print("[bold white]Select an option (NUM) > ", end = "")
            user_input = input()

            if user_input == "1":
                print(f"Current word type is: {self.config["hash_type"]}")
                print("[bold white]Enter in a new hash type (sha256, sha1, md5)[/]", end = " ")
                new_hash = input()

                if new_hash.lower() == "sha256":
                    self.config["hash_type"] = new_hash.lower()
                
                elif new_hash.lower() == "sha1":
                    self.config["hash_type"] = new_hash.lower()

                elif new_hash.lower() == "md5":
                    self.config["hash_type"] = new_hash.lower()

            elif user_input == "2":
                print("[bold white]Not supported yet. Just change the filename in config/config.json")
                input()

            elif user_input == "3":
                running = False

        cc()
        self.file_loader.save(self.config_path, self.config)

    def crack(self, hash_input: str) -> None:
        return self.hash_engine.hash_string(hash_input, self.config["hash_type"], False, self.config["wordlist_path"])

    def hash(self, hash_input: str, cracking: bool, details: bool) -> None:
        output = self.hash_engine.hash_string(hash_input, self.config["hash_type"], cracking, self.config["wordlist_path"])
        if isinstance(output, dict):
            self.file_loader.append_to_history(
                output | {"hash_input": hash_input}
            )
        else:
            self.file_loader.append_to_history(
                {"hashed_password": output}
            )

        if cracking:
            if output["cracked"]:
                if details:
                    print(f"[white bold]Hash {output["hash"]}[/]")
                    print(f"[white bold]Hash Type: {output["hash_type"]}[/]")
                    print(f"[white bold]Password: {output["cracked"]}[/]")

                else:
                    print(f"[white bold]Password: {output["cracked"]}")

            else:
                print(f"[white bold]Could not crack {hash_input}. Try a different word list?[/]")

        else:
            print(f"[white bold]{output}[/]")

    def strength(self, password: str, extra_details: bool) -> None:
        details = check_password_security(password)
        self.file_loader.append_to_history(
            details | {"password": password}
        )

        if extra_details:
            print(f"[white bold]Password grade: {details["grade"]}[/]")
            print(f"[white bold]Password length score: {details["length"]}[/]")
            print(f"[white bold]Password character variety score: {details["char_variety"]}[/]")
            print(f"[white bold]Password repeated characters score: {details["repeated_chars"]}[/]")
            print(f"[white bold]{f"{password} is not a common password" if details["common_password"] == 0 else f"{password} is a common password"}[/]")

        else:
            print(f"[white bold]Password grade: {details["grade"]}\nUse --details for more details[/]")

    def hibp(self, password: str, details: bool) -> None:
        result = hibp(password)
        self.file_loader.append_to_history(
            result | {"password": password}
        )

        if details:
            print(f"[white bold]Found {password}: {result["found"]}")
            print(f"[white bold]Breach count: {result["breach_count"]}")

        else:
            print(f"[white bold]{f"{password} has been found in data breaches" if result["found"] else f"{password} has not been found in data breaches"}[/]")

if __name__ == "__main__":
    c = CredAudit()

    parser = argparse.ArgumentParser(prog = "CredAudit")
    options = parser.add_argument_group("Options")
    password_testing = parser.add_argument_group("Testing Passwords")
    string_hashing = parser.add_argument_group("Hashing")

    options.add_argument("--config", action = "store_true", help="Change settings in the config file.")
    options.add_argument("--details", action = "store_true", help = "Get more details")

    password_testing.add_argument("--crack", nargs="?", const=True, default=None, help="Hash to audit (optional: provide a hash string, or use alone with --hash)")
    password_testing.add_argument("--strength", type = str, help = "Test a password's strength")
    password_testing.add_argument("--hibp", type = str, help = "Check if you password has been found in any breaches")

    string_hashing.add_argument("--hash", type=str, help="Hash a string (Type of hash in config.json)")

    args = parser.parse_args()

    if args.config:
        c.config_settings()
    
    # String Hashing
    elif args.hash:
        c.hash(args.hash, args.crack, args.details)
    
    # Testing Passwords
    elif args.crack:
        print(c.crack(args.crack))

    elif args.strength:
        c.strength(args.strength, args.details)

    elif args.hibp:
        c.hibp(args.hibp, args.details)

    # Help
    else:
        parser.print_help()