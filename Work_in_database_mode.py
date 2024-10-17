import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

MODE = "DATABASE"

PATH_OF_DATA = ""


# You will need to paste your certificate path and the database url in the next two path,
# instead of the fictional ones given as example
cred = credentials.Certificate("C:/Users/Mario/Downloads/long_name_with_strange_latters_and_numbers.json")
firebase_admin.initialize_app(cred,
                              {'databaseURL': 'https://url_of_your_db.firebase_something.something_else/'})


db_PASSWORDS = db.reference('PASSWORDS')
db_CHARACTERS_SETS = db.reference('CHARACTERS_SETS')
