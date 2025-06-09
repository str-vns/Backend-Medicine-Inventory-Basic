from django.http.response import HttpResponse
from dotenv import load_dotenv
import os
import pyrebase
import uuid
from firebase_admin import credentials, storage

API_KEY = str(os.getenv("API_KEY"))
AUTH_DOMAIN = str(os.getenv("AUTH_DOMAIN"))
PROJECT_ID = str(os.getenv("PROJECT_ID"))
STORAGE_BUCKET = str(os.getenv("STORAGE_BUCKET"))
MESSAGING_SENDER_ID = str(os.getenv("MESSAGING_SENDER_ID"))
APP_ID = str(os.getenv("APP_ID"))

firebaseConfig = pyrebase.initialize_app(
    {
        "apiKey": API_KEY,
        "authDomain": AUTH_DOMAIN,
        "projectId": PROJECT_ID,
        "storageBucket": STORAGE_BUCKET,
        "messagingSenderId": MESSAGING_SENDER_ID,
        "appId": APP_ID,
        "databaseURL": "",
    }
)



def upload_helper(image, path):

    uuidV4 = str(uuid.uuid4())
    storage = firebaseConfig.storage()

    storage.child(f"images/{path}/{uuidV4 + "_" + image.name}").put(image)

    url = storage.child(f"images/{path}/{uuidV4 + "_" + image.name}").get_url("")
    public_id = uuidV4 + "_" + image.name
    original_name = image.name

    return url, public_id, original_name


def delete_image_helper(image, path):

    storage = firebaseConfig.storage()
    storage.child(f"images/{path}/{image}").delete()
    return HttpResponse("Image deleted successfully")
