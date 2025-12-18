import bcrypt

def register(username, password): 
    # Generate a random salt
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password, salt)
    # Store the username and hashed password in the database
    db.insert_one({'username': username, 'password': hashed_password})

def login(username, password): 
    user = db.find_one {'username': username}
    if user: 
        return bcrypt.checkpw(password, user['password']) 
    else:
        return False