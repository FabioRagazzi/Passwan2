import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

MODE = "DATABASE"

PATH_OF_DATA = ""

cred = credentials.Certificate(r"C:\Users\Faz98\Downloads\passwan-328c1-firebase-adminsdk-cvu0a-c74cd7ed53.json")
firebase_admin.initialize_app(cred,
                              {'databaseURL': 'https://passwan-328c1-default-rtdb.europe-west1.firebasedatabase.app/'})
db_PASSWORDS = db.reference('PASSWORDS')
db_CHARACTERS_SETS = db.reference('CHARACTERS_SETS')
