import hashlib
import argparse
import json
from os.path import join

from src import *

class CredAudit:
    def __init__(self):
        self.config_path = join("config", "config.json")
        self.config = self.load_config()

        self.hashing = {
            "sha256": lambda string: hashlib.sha256(string.encode("utf-8")).hexdigest(),
            "sha1": lambda string: hashlib.sha1(string.encode("utf-8")).hexdigest(),
            "md5": lambda string: hashlib.md5(string.encode("utf-8")).hexdigest()
        }

    def load_config(self) -> dict:
        try:
            with open(self.config_path, "r") as f:
                return json.load(f)

        except FileNotFoundError:
            print(f"Config filepath invalid")
            exit(1)

    def hash_string(self, string: str, crack: bool) -> str | dict:
        return self.hashing[self.config["hash_type"]](string) if not crack else self.audit(self.hashing[self.config["hash_type"]](string))

    def audit(self, hash_input: str) -> str:
        if not self.config["wordlist_path"]:
            print("Word List file in config.json is empty")
            return ""

        if not hash_input:
            print("Hash input can't be empty")
            return ""

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
    c = CredAudit()

    parser = argparse.ArgumentParser(prog = "CredAudit")
    parser.add_argument("--config", action="store_true", help="Change settings in the config file.")
    parser.add_argument("--crack", nargs="?", const=True, default=None, help="Hash to audit (optional: provide a hash string, or use alone with --hash)")
    parser.add_argument("--hash", type=str, help="Hash a string (Type of hash in config.json)")
    
    args = parser.parse_args()

    if args.config:
        # c.config()
        pass

    elif args.hash:
        print(c.hash_string(args.hash, args.crack))

    elif args.crack:
        if isinstance(args.crack, bool):
            print("Must use a hash string with just --crack")
            exit(1)
        print(c.audit(args.crack))

    else:
        parser.print_help()