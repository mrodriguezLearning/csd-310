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

def report_average_assets(cursor):
    print("\n--- REPORT 2: AVERAGE CLIENT ASSETS ---")
    query = "SELECT AVG(total_assets) FROM client;"
    cursor.execute(query)
    result = cursor.fetchone()
    print(f"Average Assets per Client: ${result[0]:,.2f}")



try:
    db = mysql.connector.connect(**config)
    cursor = db.cursor()

    
    report_average_assets(cursor)

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