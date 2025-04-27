# If you have pip installed type pip install psycopg2
# If you are not using pip you can install via apt install python3-psycopg2
# You should not need to run this as sudo or root. It will read the config.conf file but not edit it.
import os
import re
import psycopg2
from psycopg2 import sql
from datetime import datetime

backup_folder = "/home/debian/fusionbackup/"

# Function to delete files older than 7 days
def delete_old_files(folder_path, days_old=7):
    current_time = time.time()
    cutoff_time = current_time - (days_old * 86400)  # 86400 seconds in a day

    try:
        # Loop through all files in the folder
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            
            # Check if it's a file and if it's older than the cutoff time
            if os.path.isfile(file_path):
                file_mod_time = os.path.getmtime(file_path)
                
                if file_mod_time < cutoff_time:
                    # Delete the file if it is older than 7 days
                    os.remove(file_path)
                    print(f"Deleted old file: {filename}")
                    
    except Exception as e:
        print(f"Error deleting old files: {e}")

# Database connection details
db_host = "localhost"  # Change as necessary
db_port = 5432         # Change as necessary
db_name = "fusionpbx"  # Change as necessary
db_user = "fusionpbx"

# Path to the config file
config_file_path = "/etc/fusionpbx/config.conf"

# Function to get the password from the config file
def get_db_password(config_file_path):
    password = None
    try:
        with open(config_file_path, 'r') as file:
            for line in file:
                # Look for the line containing the password
                if line.startswith("database.0.password"):
                    # Extract the password using regex
                    match = re.search(r"database\.0\.password\s*=\s*(\S+)", line)
                    if match:
                        password = match.group(1)
                        break
    except FileNotFoundError:
        print(f"Error: The file {config_file_path} does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")
    
    return password

# Function to test the database connection
def test_db_connection(db_host, db_port, db_name, db_password):
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(
            dbname=db_name,
            user=db_user,  # Adjust with your actual username
            password=db_password,
            host=db_host,
            port=db_port
        )
        print("Connection successful.")
        conn.close()
    except Exception as e:
        print(f"Error connecting to the database: {e}")

# Function to export the database to a file
def export_db_to_file(db_host, db_port, db_name, db_password, backup_folder):
    # Create the folder if it doesn't exist
    if not os.path.exists(backup_folder):
        os.makedirs(backup_folder)

    # Create the backup file name based on the current date and time
    backup_filename = f"{db_name}_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sql"
    backup_file_path = os.path.join(export_folder, backup_filename)

    # Command to export the database
    dump_command = f"pg_dump -h {db_host} -p {db_port} -U {db_user} -F c -b -v -f {backup_file_path} {db_name}"

    try:
        # Run the pg_dump command
        os.environ["PGPASSWORD"] = db_password
        os.system(dump_command)
        print(f"Database backup exported to {backup_file_path}")
    except Exception as e:
        print(f"Error exporting the database: {e}")

# Main function
def main():
    # Get the password from the config file
    db_password = get_db_password(config_file_path)
    
    if db_password:
        # Test the database connection
        test_db_connection(db_host, db_port, db_name, db_password)
        
        # Export the database
        backup_folder = "/home/debian/fusionbackup/"
        os.makedirs(backup_folder, exist_ok=True)
        export_db_to_file(db_host, db_port, db_name, db_password, backup_folder)
    else:
        print("Failed to retrieve the database password from the config file.")

# Run the main function
if __name__ == "__main__":
    main()