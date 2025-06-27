import argparse
from backend.cracker import crack_hash, pass_strength 
import time

def main():
    parser =argparse.ArgumentParser(description = "HashHunt - Password Hash Cracker")

    parser.add_argument("--hash", required=True, help="Target hash to crack")
    parser.add_argument("--wordlist", required=True, help="Path to wordlist file")
    parser.add_argument("--algo", default="sha256", choices=["sha256","md5","sha1"], help="Hashing algorithm (Default: sha256)")
    parser.add_argument("--check-password", help="Check if your password is strong and guessable")


    args = parser.parse_args()

    if args.check_password:
        result = pass_strength(args.check_password, args.wordlist, args.algo)

        print(f"🔐 Password strength: {result['strength']}")
        print(f"🎯 Is it guessable (in wordlist)? {'Yes' if result['guessable'] else 'No'}")
        return  # exit after running this mode


    start_time = time.time()
    result = crack_hash(args.hash, args.wordlist, args.algo)
    end_time = time.time()

    duration = end_time - start_time

    if result:
        print(f"Password Found: {result}")

    else:
        print("Password Not Found in wordlist")

    print(f"Time Taken: {duration:.4f} seconds")

if __name__ == "__main__":
    main()        