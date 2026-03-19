import hashlib
import argparse
import json
from os.path import join

from src import *

class CredAudit:
    def __init__(self):
        self.config_path = join("config", "config.json")

    def load_config(self) -> dict:
        try:
            with open(self.config_path, "r") as f:
                return json.load(f)

        except FileNotFoundError:
            print(f"Config filepath invalid")
            exit(1)

    def run_audit(self, hash_input: str) -> str:
        hash_type = identify_hash(hash_input)
        config = self.load_config()

        cracked = None
        if hash_type != "Unknown" and hash_type != "bcrypt":
            print("Cracking...")
            cracked = crack_hash(hash_input, hash_type, config["wordlist_path"])
            print(f"Cracked: {cracked}" if cracked else "Not found in wordlist.")

        result = {
            "hash": hash_input,
            "hash_type": hash_type,
            "cracked": cracked
        }

        return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog = "CredAudit")
    parser.add_argument("--config", action = "store_true", help = "Change settings in the config file.")
    parser.add_argument("--hash", type = str, help = "Hash to audit")
    
    args = parser.parse_args()

    if args.config:
        pass

    elif args.hash:
        result = ""

    else:
        parser.print_help()