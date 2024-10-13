import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate(r"C:\Users\Faz98\Downloads\passwan-328c1-firebase-adminsdk-cvu0a-c74cd7ed53.json")
firebase_admin.initialize_app(cred,
                              {'databaseURL': 'https://passwan-328c1-default-rtdb.europe-west1.firebasedatabase.app/'})

# Clear all data in the database
ref = db.reference('/')  # Reference to the root node
ref.delete()  # Deletes everything under the root node

print("Database cleared successfully.")
