import hashlib
import re

from .helpers import FileLoader

# TODO: Increase speed with concurrent.futures
def crack_hash(target: str, hash_type: str, word_path: str) -> None | str:
    hashes = {
        "SHA256": lambda string: hashlib.sha256(string.encode("utf-8")).hexdigest(),
        "SHA1": lambda string: hashlib.sha1(string.encode("utf-8")).hexdigest(),
        "MD5": lambda string: hashlib.md5(string.encode("utf-8")).hexdigest()
    }
    
    try:
        hash_func = hashes.get(hash_type, None)
        if hash_func is None:
            return None

        with open(word_path, "r", encoding = "utf-8", errors = "ignore") as f:
            for word in f:
                word = word.strip()

                attempt = hash_func(word)

                if attempt == target:
                    return word

    except FileNotFoundError as ex:
        print(f"[+] Word path {word_path} is an invalid path: {ex}")
        return None
    
    return None

def identify_hash(hash: str) -> str:
    hash_string = hash.strip()
    length = len(hash_string)

    if hash_string.startswith("$2b$") or hash_string.startswith("$2a$"):
        return "bcrypt"

    if re.fullmatch(r'[a-fA-F0-9]+', hash_string):
        if length == 32:
            return "MD5"

        elif length == 40:
            return "SHA1"

        elif length == 64:
            return "SHA256"

    return "Unknown"

class HashingEngine:
    def __init__(self) -> None:
        self.file_loader = FileLoader()

        self.hashing = {
            "sha256": lambda string: hashlib.sha256(string.encode("utf-8")).hexdigest(),
            "sha1": lambda string: hashlib.sha1(string.encode("utf-8")).hexdigest(),
            "md5": lambda string: hashlib.md5(string.encode("utf-8")).hexdigest()
        }
    
    def hash_string(self, string: str, type: str, crack: bool, wordlist_path: str) -> str | dict:
        return self.hashing[type](string) if not crack else self.audit(self.hashing[type](string), wordlist_path)

    def audit(self, hash_input: str, wordlist_path: str) -> dict:
        hash_type = identify_hash(hash_input)
        
        cracked = None
        if hash_type != "Unknown" and hash_type != "bcrypt":
            cracked = crack_hash(hash_input, hash_type, wordlist_path)
        
        result = {
            "hash": hash_input,
            "hash_type": hash_type,
            "cracked": cracked
        }

        return result