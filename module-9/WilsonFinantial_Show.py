import mysql.connector
from mysql.connector import errorcode

import dotenv # to use .env file
from dotenv import dotenv_values

#using our .env file
secrets = dotenv_values(".env")

# Configuration using your local credentials
config = {
    "user": secrets["USER"],
    "password": secrets["PASSWORD"],
    "host": secrets["HOST"],
    "database": secrets["DATABASE"],
    "raise_on_warnings": True #not in .env file
}

def display_table_contents(cursor, table_name):
    print(f"\n--- DISPLAYING {table_name.upper()} RECORDS ---")
    cursor.execute(f"SELECT * FROM {table_name}")
    
    # Fetch column names
    columns = [desc[0] for desc in cursor.description]
    
    rows = cursor.fetchall()
    for row in rows:
        for i in range(len(columns)):
            print(f"{columns[i]}: {row[i]}")
        print("-" * 20)

try:
    db = mysql.connector.connect(**config)
    cursor = db.cursor()

    tables = ['employee', 'billing_structure', 'client', 'transaction', 'appointment']
    
    for table in tables:
        display_table_contents(cursor, table)

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Invalid username or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
finally:
    if 'db' in locals() and db.is_connected():
        cursor.close()
        db.close()
        print("\nDatabase connection closed.")