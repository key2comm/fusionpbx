import psycopg2
# If you have pip installed type pip install psycopg2
# If you are not using pip you can install via apt install python3-psycopg2
import re
import subprocess
import os

# Define the database connection details as variables
DB_HOST = '127.0.0.1'        # Host
DB_USER = 'fusionpbx'        # Username
DB_NAME = 'fusionpbx'        # Database name
DB_PORT = 5432               # Port

# Define the path to the config file
config_file_path = '/etc/fusiobpbx/config.php'

# Function to get the database password from the config file
def get_database_password(config_file_path):
    try:
        with open(config_file_path, 'r') as file:
            # Read all lines from the file
            lines = file.readlines()
            
            # Iterate through each line and search for the pattern 'database.0.password'
            for line in lines:
                if line.strip().startswith('database.0.password'):
                    # Use regex to extract the password after '='
                    match = re.search(r'=\s*(\S+)', line)
                    if match:
                        return match.group(1)
            # If the password is not found
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Function to test the database connection
def test_database_connection(username, password, host, port):
    try:
        # Create a connection to the PostgreSQL database
        connection = psycopg2.connect(
            dbname=DB_NAME,  
            user=DB_USER,
            password=password,
            host=DB_HOST,
            port=DB_PORT
        )
        
        # If the connection is successful, return True
        print("Database connection successful.")
        connection.close()  # Close the connection
        return True
    except Exception as e:
        # If connection fails, print the error
        print(f"Database connection failed: {e}")
        return False

# Main logic
password = get_database_password(config_file_path)

if password:
    print("Database password found. Testing connection...")
    if test_database_connection(DB_USER, password, DB_HOST, DB_PORT):
        print("Connection test successful!")
    else:
        print("Connection test failed.")
else:
    print("Password not found in the config file.")