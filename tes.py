import mysql.connector
import hashlib

# MySQL database configuration
db_config = {
    'host': 'localhost',
    'user': 'your_username',
    'password': 'your_password',
    'database': 'infocusstudio'
}

# Function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to verify passwords
def verify_password(hashed_password, password):
    return hashed_password == hashlib.sha256(password.encode()).hexdigest()

# Function to authenticate user
def authenticate(username, password):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        # Query the database to retrieve the user's hashed password
        cursor.execute('SELECT password FROM clients WHERE username = %s', (username,))
        user = cursor.fetchone()

        if user:
            hashed_password = user['password']
            if verify_password(hashed_password, password):
                return True

    except mysql.connector.Error as err:
        print("Error connecting to MySQL database:", err)

    finally:
        # Close database connection
        cursor.close()
        conn.close()

    return False


