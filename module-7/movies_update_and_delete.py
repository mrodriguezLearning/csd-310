"""
Marco Rodriguez Gomez
04/23/2026
Assignment: Movies: Update & Deletes
"""

import mysql.connector
from dotenv import dotenv_values

secrets = dotenv_values(".env")

config = {
    "user": secrets["USER"],
    "password": secrets["PASSWORD"],
    "host": secrets["HOST"],
    "database": secrets["DATABASE"],
    "raise_on_warnings": True
}

def show_films(cursor, title):
    # method to execute an inner join on all tables,
    # iterate over the dataset and output the results to the terminal window.

    # inner join query
    query = """SELECT 
               film_name as Name, film_director as Director, genre_name as Genre, studio_name as 'Studio Name' 
               FROM film
                INNER JOIN genre ON film.genre_id = genre.genre_id
                INNER JOIN studio ON film.studio_id = studio.studio_id"""
    # execute the query
    cursor.execute(query)

    # get the results from the cursor object
    films = cursor.fetchall()

    print("\n -- {} --".format(title))

    # iterate over the film data set and display the results
    for film in films:
        print("Film Name: {}\nDirector: {}\nGenre Name ID: {}\nStudio Name: {}\n".format(film[0], film[1], film[2], film[3]))

db = None

try:
    db = mysql.connector.connect(**config)
    cursor = db.cursor()

    # 1. Display initial films
    show_films(cursor, "DISPLAYING FILMS")

    # 2. Insert a new record into the film table
    # Using Jurassic Park with Universal Pictures (studio_id 3) and SciFi (genre_id 2)
    insert_query = """INSERT INTO 
        film (film_name, film_releaseDate, film_runtime, film_director, studio_id, genre_id) 
        VALUES ('Jurassic Park', '1993', 127, 'Steven Spielberg', 3, 2)"""
    cursor.execute(insert_query)
    db.commit()

    # 3. Display films after insert
    show_films(cursor, "DISPLAYING FILMS AFTER INSERT")

    # 4. Update the film Alien to being a Horror film
    # Horror is genre_id 1
    update_query = "UPDATE film SET genre_id = 1 WHERE film_name = 'Alien'"
    cursor.execute(update_query)
    db.commit()

    # 5. Display films after update
    show_films(cursor, "DISPLAYING FILMS AFTER UPDATE- Changed Alien to Horror")

    # 6. Delete the movie Gladiator
    delete_query = "DELETE FROM film WHERE film_name = 'Gladiator'"
    cursor.execute(delete_query)
    db.commit()

    # 7. Display films after delete
    show_films(cursor, "DISPLAYING FILMS AFTER DELETE")

except mysql.connector.Error as err:
    print(err)

finally:
    if db is not None:
        cursor.close()
        db.close()