from collections import Counter
from os.path import join

def check_password_security(password: str) -> dict:
    grades = {
        (0, 35): "WEAK",
        (36, 57): "FAIR",
        (58, 79): "STRONG",
        (80, 100): "VERY STRONG"
    }
    lengths = {
        6: 0,
        8: 10,
        12: 20,
        16: 30
    }
    assessment = {
        "length": 0,
        "char_variety": 0,
        "repeated_chars": 0,
        "common_password": 0,
        "total": 0,
        "grade": ""
    }

    # Length
    #region
    for l in [6, 8, 12, 16]:
        if len(password) < l:
            assessment["length"] = lengths[l]
            break
    else:
        assessment["length"] = 40

    if any(char.islower() for char in password):
        assessment["char_variety"] += 5

    if any(char.isupper() for char in password):
        assessment["char_variety"] += 5

    if any(char.isdigit() for char in password):
        assessment["char_variety"] += 5
    
    if any(not char.isalnum() and not char.isspace() for char in password):
        assessment["char_variety"] += 5
    #endregion

    # Repeated Characters
    #region
    items = Counter(password)

    repeated = sum(1 for item in items if items[item] > 1)
    percentage = (repeated / len(password)) * 100

    if percentage < 25:
        assessment["repeated_chars"] = 0
    
    elif percentage < 50:
        assessment["repeated_chars"] = -5

    elif percentage < 75:
        assessment["repeated_chars"] = -10

    else:
        assessment["repeated_chars"] = -20
    #endregion

    # Common Passwords
    #region
    try:
        with open(join("word_lists", "common.txt")) as f:
            common_passwords = f.readlines()
            common_passwords = [passwd.strip("\n") for passwd in common_passwords]
        
        if password in common_passwords:
            assessment["common_password"] = -20
    
    except FileNotFoundError:
        print("Common.txt not found.")
    #endregion

    # Calc Total
    assessment["total"] = assessment["char_variety"] + assessment["common_password"] + assessment["length"] + assessment["repeated_chars"]
    assessment["total"] = max(0, min(assessment["total"], 100))

    for x, y in grades.keys():
        if x <= assessment["total"] <= y:
            assessment["grade"] = grades[(x, y)]

    return assessment

