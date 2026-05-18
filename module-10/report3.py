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

def report_high_volume_clients(cursor):
    print("\n--- REPORT 3: HIGH-VOLUME TRANSACTION CLIENTS (>10/MONTH) ---")
    query = """
        SELECT 
    c.f_name, 
    c.l_name,
    DATE_FORMAT(t.transaction_date, '%Y-%m') AS Transaction_Month,
    COUNT(t.transaction_id) AS Transaction_Count
FROM client c
JOIN transaction t ON c.client_id = t.client_id
GROUP BY c.client_id, c.f_name, c.l_name, Transaction_Month
HAVING Transaction_Count > 10
ORDER BY Transaction_Month DESC, Transaction_Count DESC;
    """
    cursor.execute(query)
    results = cursor.fetchall()
    if not results:
        print("No clients exceeded 10 transactions this month.")
    for row in results:
        print(f"Client: {row[0]} {row[1]} | Transactions: {row[2]}")



try:
    db = mysql.connector.connect(**config)
    cursor = db.cursor()

    
    report_high_volume_clients(cursor)

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