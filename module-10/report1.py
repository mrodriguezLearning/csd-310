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

def report_client_growth(cursor):
    print("\n--- REPORT 1: CLIENT GROWTH (PAST 6 MONTHS) ---")
    query = """
        SELECT DATE_FORMAT(join_date, '%Y-%m') AS Month, COUNT(client_id) AS New_Clients
        FROM client
        WHERE join_date >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH)
        GROUP BY Month
        ORDER BY Month DESC;
    """
    cursor.execute(query)
    results = cursor.fetchall()
    for row in results:
        print(f"Month: {row[0]} | New Clients: {row[1]}")


try:
    db = mysql.connector.connect(**config)
    cursor = db.cursor()

    
    report_client_growth(cursor)

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