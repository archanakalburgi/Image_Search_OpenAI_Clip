import sqlite3
import os

connection = sqlite3.connect('database.db')
script_path  = os.path.join(os.path.dirname(__file__), 'schema.sql')


with open(script_path) as f:
    connection.executescript(f.read())

cur = connection.cursor()


"""
Later load default images
"""
# cur.execute("INSERT INTO images (title, image_path) VALUES (?, ?)",
#             ('First Image', 'images/first.png')
#         )


# cur.execute("INSERT INTO images (title, image_path) VALUES (?, ?)",
#              ('Second Image', 'images/second.png')
#             )

# cur.execute("INSERT INTO images (title, image_path) VALUES (?, ?)",
#              ('Third Image', 'images/second.png')
#             )

# cur.execute("INSERT INTO images (title, image_path) VALUES (?, ?)",
#              ('Fourth Image', 'images/second.png')
#             )

connection.commit()
connection.close()