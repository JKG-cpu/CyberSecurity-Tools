import hashlib

def crack_hash(target: str, hash_type: str, word_path: str) -> None | str:
    try:
        with open(word_path, "r", encoding = "utf-8", errors = "ignore") as f:
            for word in f:
                word = word.strip()

                if hash_type == "SHA256":
                    attempt = hashlib.sha256(word.encode('utf-8')).hexdigest()

                elif hash_type == "SHA1":
                    attempt = hashlib.sha1(word.encode('uft-8')).hexdigest()

                elif hash_type == "MD5":
                    attempt = hashlib.md5(word.encode('uft-8')).hexdigest()

                else:
                    return None

                if attempt == target:
                    return word

    except FileNotFoundError as ex:
        print(f"[+] Word path {word_path} is an invalid path: {ex}")
        return None
    
    return None
    