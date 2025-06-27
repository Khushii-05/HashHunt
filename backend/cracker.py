import hashlib
import re
from tqdm import tqdm

def crack_hash(target_hash, wordlist, algo="sha256"):
    with open(wordlist,"r") as file:
        lines = file.readlines()

    for word in tqdm(lines, desc="Cracking Progress"):        
            word = word.strip()
            if algo == "sha256":
                hashed = hashlib.sha256(word.encode()).hexdigest()
            elif algo == "md5":
                hashed = hashlib.md5(word.encode()).hexdigest()
            elif algo == "sha1":
                hashed = hashlib.sha1(word.encode()).hexdigest()
            else:
                raise ValueError("Unsupported algorithm")    
            if hashed == target_hash:
                return word   #pass found
    return None   #pass not found
        

def pass_strength(password, wordlist,algo="sha256" ):

    # check if password is guessable 
    guessable = False 
    target_hash = None

    with open(wordlist, "r") as file:

        for line in file:
            guess = line.strip()

            if algo == "sha256":
                hashed_guess = hashlib.sha256(guess.encode()).hexdigest()
                target_hash = hashlib.sha256(password.encode()).hexdigest()
            elif algo == "md5":
                hashed_guess = hashlib.md5(guess.encode()).hexdigest()
                target_hash = hashlib.md5(password.encode()).hexdigest()
            elif algo == "sha1":
                hashed_guess = hashlib.sha1(guess.encode()).hexdigest()
                target_hash = hashlib.sha1(password.encode()).hexdigest()
            else:
                raise ValueError("Unsupported algorithm")    
            if hashed_guess == target_hash:
               
               guessable= True
               break  #pass found in wordlist

    # Password strength logic
    length = len(password)
    has_upper = bool(re.search(r"[A-Z]", password))
    has_lower = bool(re.search(r"[a-z]", password))
    has_digit = bool(re.search(r"[0-9]", password))
    has_symbol = bool(re.search(r"[!@#$%^&*(),.?\":{}|<>]", password))

    score = sum([has_upper, has_lower, has_digit, has_symbol])

    if length < 6:
        strength = "Very Weak"
    elif length >= 6 and score < 2:
        strength = "Weak"
    elif length >= 8 and score == 2:
        strength = "Moderate"
    elif length >= 10 and score == 3:
        strength = "Strong"
    elif length >= 12 and score == 4:
        strength = "Very Strong"
    else:
        strength = "Moderate"

    return {
        "guessable": guessable,
        "strength": strength
    }
    
