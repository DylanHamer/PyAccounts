import hashlib  # Create password hashes
import pickle   # Serialize account data
import getpass  # Get passwords securely
import pathlib  # Manage file paths

def genHash(plaintext):
    plaintext = plaintext.encode()               # Encode plaintext
    hashed = hashlib.md5(plaintext).hexdigest()  # Create MD5 hash 
    return hashed

def newUserAccount():
    account = {}
    account["name"] = input("Please enter your full name: ").split(" ")
    accountCreated = False
    while not accountCreated:
        account["username"] = input("Please enter a username: ")
        account["password"] = genHash(getpass.getpass())
        accountFilePath = genHash(account["username"]) + ".act"
        if pathlib.Path(accountFilePath).is_file():  # Check if file exists
            print("Sorry, an account with this username already exists. Please choose another username.")
        else:
            with open(accountFilePath, "wb") as accountFile:
                pickle.dump(account, accountFile)  # Serialise account data to a file
                accountCreated = True

def checkUserAccount():
    username = input("Please enter your username: ")
    password = genHash(getpass.getpass())
    try:
        account = pickle.load(open(genHash(username) + ".act", "rb"))
        if account["password"] == password:
            return account
        else:
            print("Incorrect username or password!")
    except:
        print("Incorrect username or password!")
        


newUserAccount()
print(checkUserAccount())
                                    
    
