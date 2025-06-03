import functions_framework
import firebase_admin
from firebase_admin import credentials, firestore
from flask import abort

cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred)
db = firestore.client()

@functions_framework.http
def set_user_level(request):
    if request.method != "POST":
        return ("Method Not Allowed", 405)
    data = request.get_json(silent=True)
    if not data or "userId" not in data or "level" not in data:
        return ("Bad Request: missing userId or level", 400)
    user_id = data["userId"]
    level = data["level"]
    db.collection("users").document(user_id).set({"level": level}, merge=True)
    return {"status": "success"}, 200
