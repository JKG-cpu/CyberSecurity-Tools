import re

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

