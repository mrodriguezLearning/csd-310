"""
Marco Rodriguez Gomez
04/16/2026
Assignment: Movies: Table Queries
"""

import mysql.connector
from mysql.connector import errorcode
from dotenv import dotenv_values

# Load database credentials
secrets = dotenv_values(".env")

config = {
    "user": secrets["USER"],
    "password": secrets["PASSWORD"],
    "host": secrets["HOST"],
    "database": secrets["DATABASE"],
    "raise_on_warnings": True
}

db = None

try:
    db = mysql.connector.connect(**config)
    cursor = db.cursor()

    # -- QUERY 1: Select all fields for the studio table
    print("-- DISPLAYING Studio RECORDS --")
    cursor.execute("SELECT studio_id, studio_name FROM studio")
    for (studio_id, studio_name) in cursor:
        print(f"Studio ID: {studio_id}")
        print(f"Studio Name: {studio_name}\n")

    # -- QUERY 2: Select all fields for the genre table
    print("-- DISPLAYING Genre RECORDS --")
    cursor.execute("SELECT genre_id, genre_name FROM genre")
    for (genre_id, genre_name) in cursor:
        print(f"Genre ID: {genre_id}")
        print(f"Genre Name: {genre_name}\n")

    # -- QUERY 3: Select movie names with runtime < 2 hours (120 minutes)
    print("-- DISPLAYING Short Film RECORDS --")
    # Filter by film_runtime < 120
    cursor.execute("SELECT film_name, film_runtime FROM film WHERE film_runtime < 120")
    for (film_name, film_runtime) in cursor:
        print(f"Film Name: {film_name}")
        print(f"Runtime: {film_runtime}\n")

    # -- QUERY 4: List film names and directors grouped (ordered) by director
    print("-- DISPLAYING Director RECORDS in Order --")
    # Using ORDER BY to group records by director name
    cursor.execute("SELECT film_name, film_director FROM film ORDER BY film_director DESC")
    for (film_name, film_director) in cursor:
        print(f"Film Name: {film_name}")
        print(f"Director: {film_director}\n")

    input("Press any key to exit...")

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Invalid username or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)

finally:
    if db is not None:
        cursor.close()
        db.close()