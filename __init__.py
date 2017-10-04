import bcrypt
import getpass
import pickle
import string
import click
import pathlib

def getPassword():
    symbols = 0
    numbers = 0
    uppers = 0
    created = False
    while not created:
        password = getpass.getpass()  # Get password without echoing
        for symbol in string.punctuation:
            symbols += password.count(symbol)   
        for number in string.digits:
            numbers += password.count(number)
        for upper in string.ascii_uppercase:
            uppers += password.count(upper)
        if symbols or numbers and uppers and len(password) >= 8:
            verify = getpass.getpass("Please confirm your password: ")
            if password == verify:
                created = True
            else:
                click.secho("Passwords do not match", fg = "red")
        else:
            click.secho("Password must have at least 1 symbol, 1 number, 1 uppercase character and be at least 8 characters long", fg = "red")
    return password.encode()
          
def hashPassword(password, hash = False):
    if hash:  # If a hash is provided:
        salt = hash  # Use the salt contained within the hash
    else:  # If a hash is not provided:
        salt = bcrypt.gensalt()  # Generate a salt using bcrypt
    hash = bcrypt.hashpw(password, salt)  # Hash the password using the generated salt
    return hash

def generateAccount():
    account = {}
    account["name"] = input("Please enter your full name: ").split(" ")
    created = False
    while not created:
        account["username"] = input("Please choose a username: ")
        account["password"] = hashPassword(getPassword())
        if pathlib.Path(account["username"] + ".act").exists():
            click.secho("An account with this username already exists", fg = "red")
        else:
            created = True
    return account

def storeAccount():
    account = generateAccount()
    try:
        with open(account["username"] + ".act", "wb") as accountFile:
            pickle.dump(account, accountFile)
    except:
        click.secho("An error occurred while creating the account file", fg = "red")

def loadAccount(accountPath):
    try:
        with open(accountPath) as accountFile:
            account = pickle.load(accountFile)
            return account
    except:
         click.secho("Invalid username or password", fg = "red")
         exit()
    return account

def verifyAccount():
    username = input("Please enter your username: ")
    password = getpass.getpass()
    account = loadAccount(username + ".act")
    if bcrypt.checkpw(password, account["password"]):
        click.secho("Welcome back, "+account["name"][0], fg = "green")
    else:
        click.secho("Invalid username or password", fg = "red")

