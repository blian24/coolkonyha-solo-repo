import bcrypt
import stdiomask

def generate_hash():
    print("CoolKonyha Password Hasher")
    print("--------------------------")
    
    while True:
        username = input("Enter username (or press Enter to quit): ")
        if not username:
            break
            
        password = stdiomask.getpass(prompt=f"Enter password for '{username}': ")
        confirm = stdiomask.getpass(prompt="Confirm password: ")
        
        if password != confirm:
            print("Error: Passwords do not match. Try again.\n")
            continue
            
        # Generate salt and hash
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        
        print(f"\nSUCCESS! Copy the line below into your .streamlit/secrets.toml:\n")
        print(f'{username} = "{hashed.decode("utf-8")}"')
        print("\n" + "-"*30 + "\n")

if __name__ == "__main__":
    try:
        generate_hash()
    except KeyboardInterrupt:
        print("\nExiting...")
