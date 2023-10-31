import bcrypt
# make sure have the bcrypt library installed! I got it using pip in my terminal
# but I'm not sure if the method to download is different on windows

# salting and hashing the pasword
def generate_password_hash(password):
    # salt
    salt = bcrypt.gensalt()
    
    # hash
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

 # Return the hashed password and salt
    return hashed_password, salt

# checking the password hash matches
def check_password(password, stored_password_hash, salt):
    # Hash the entered password with the stored salt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt.encode('utf-8'))
    
    # Check if the hashed password matches the stored hash
    return hashed_password == stored_password_hash

if __name__ == "__main__":
    # Generate hash and salt
    password = "user_password"
    hashed_password, salt = generate_password_hash(password)
    
    # storing the hash (obviously this will be in the database when it is set up)
    stored_password_hash = hashed_password.decode('utf-8')
    
    # User login: Check if the entered password matches the stored hash
    entered_password = input("Enter your password: ")
    if check_password(entered_password, stored_password_hash, salt):
        correctPassword = True
        # This variable is just a placeholder for now so that VS code doesn't tell me there are errors
    else:
        correctPassword = False