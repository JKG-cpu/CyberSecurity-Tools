import hashlib
import argparse
from rich import print
from os.path import join

from src import *

class CredAudit:
    def __init__(self):
        self.file_loader = FileLoader()
        self.hash_engine = HashingEngine()

        self.config_path = join("config", "config.json")
        self.config = self.file_loader.load(self.config_path)

    # Commands
    def config_settings(self) -> None:
        pass

    def crack(self, hash_input: str) -> None:
        return self.hash_engine.hash_string(hash_input, self.config["hash_type"], False, self.config["wordlist_path"])

    def hash(self, hash_input: str, cracking: bool, details: bool) -> None:
        output = self.hash_engine.hash_string(hash_input, self.config["hash_type"], cracking, self.config["wordlist_path"])

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
        details = strength_checker(password)

        if extra_details:
            print(f"[white bold]Password grade: {details["grade"]}[/]")
            print(f"[white bold]Password length score: {details["length"]}[/]")
            print(f"[white bold]Password character variety score: {details["char_variety"]}[/]")
            print(f"[white bold]Password repeated characters score: {details["repeated_chars"]}[/]")
            print(f"[white bold]{f"{password} is not a common password" if details["common_password"] == 0 else f"{password} is a common password"}[/]")

        else:
            print(f"[white bold]Password grade: {details["grade"]}\nUse --details for more details[/]")


if __name__ == "__main__":
    c = CredAudit()

    parser = argparse.ArgumentParser(prog = "CredAudit")
    parser.add_argument("--config", action = "store_true", help="Change settings in the config file.")
    parser.add_argument("--details", action = "store_true", help = "Get more details")

    parser.add_argument("--crack", nargs="?", const=True, default=None, help="Hash to audit (optional: provide a hash string, or use alone with --hash)")
    parser.add_argument("--hash", type=str, help="Hash a string (Type of hash in config.json)")
    parser.add_argument("--strength", type = str, help = "Test a password's strength")

    args = parser.parse_args()

    if args.config:
        c.config_settings()

    elif args.hash:
        c.hash(args.hash, args.crack, args.details)

    elif args.crack:
        if isinstance(args.crack, bool):
            print("Must use a hash string with just --crack")
            exit(1)
        print(c.crack(args.crack))

    elif args.strength:
        c.strength(args.strength, args.details)

    else:
        parser.print_help()