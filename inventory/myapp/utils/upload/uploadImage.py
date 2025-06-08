from django.http.response import HttpResponse
from dotenv import load_dotenv
import pyrebase
import uuid
import firebase_admin
from firebase_admin import credentials, storage

load_dotenv()

print(load_dotenv())
firebaseConfig = pyrebase.initialize_app(
    {
        "apiKey": "",
        "authDomain": "",
        "projectId": "",
        "storageBucket": "",
        "messagingSenderId": "",
        "appId": "",
        "databaseURL": "",
    }
)



def upload_helper(image, path):

    uuidV4 = str(uuid.uuid4())
    storage = firebaseConfig.storage()

    storage.child(f"images/{path}/{uuidV4 + "_" + image.name}").put(image)

    url = storage.child(f"images/{path}/{image.name}").get_url("")
    public_id = uuidV4 + "_" + image.name
    original_name = image.name

    return url, public_id, original_name


def delete_image_helper(image, path):

    storage = firebaseConfig.storage()
    storage.child(f"images/{path}/{image}").delete()
    return HttpResponse("Image deleted successfully")
