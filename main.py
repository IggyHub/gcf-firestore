from fastapi import FastAPI, HTTPException, Body
import firebase_admin
from firebase_admin import credentials, firestore
import uvicorn

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

app = FastAPI()

@app.get("/get-data/{user_id}")
def get_data(user_id: str):
    doc = db.collection("users").document(user_id).get()
    if not doc.exists:
        raise HTTPException(status_code=404, detail="User not found")
    return doc.to_dict()

@app.post("/set-data/{user_id}")
def set_data(user_id: str, data: dict = Body(...)):
    db.collection("users").document(user_id).set(data)
    return {"status": "success"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080)
