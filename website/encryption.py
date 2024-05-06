import bcrypt
# salting and hashing the pasword
def generate_password_hash(password):
    # salt
    salt = bcrypt.gensalt()
    
    # hash
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)


    # Return the hashed password and salt
    return hashed_password.decode('utf-8'), salt.decode('utf-8')

# checking the password hash matches
def check_password(password, stored_password_hash, salt):
    # Hash the entered password with the stored salt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt.encode('utf-8'))
    hashed_password = hashed_password.decode('utf-8')


    # Check if the hashed password matches the stored hash
    return hashed_password == stored_password_hash