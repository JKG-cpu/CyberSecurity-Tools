import requests
from hashlib import sha1

def hibp(password: str) -> dict:
    hashed_password = sha1(password.encode("utf-8")).hexdigest()
    prefix, suffix = hashed_password[:5], hashed_password[5:]

    r = requests.get(f"https://api.pwnedpasswords.com/range/{prefix}")
    breached_passwords = r.text.splitlines()
    
    count = 0
    for pwd in breached_passwords:
        s, c = pwd.split(":")
        if s == suffix.upper():
            count = int(c)
            break

    return {
        "found": count > 0,
        "breach_count": count
    }