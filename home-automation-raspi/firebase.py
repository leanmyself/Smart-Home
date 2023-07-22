import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


cred = credentials.Certificate('firebase-listener/ServiceAccount.json')
app = firebase_admin.initialize_app(cred)

firestore_client = firestore.client()