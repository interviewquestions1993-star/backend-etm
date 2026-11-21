import os
import sys

sys.path.append('d:/AI-Exam-preparer-v1/backendv2')
from config import FIRESTORE_HISTORY_COLLECTION, FIREBASE_COLLECTION
from firebase_client import get_firestore_client

client = get_firestore_client()
coll = client.collection(FIRESTORE_HISTORY_COLLECTION or FIREBASE_COLLECTION)
docs = coll.limit(1).stream()
for d in docs:
    data = d.to_dict()
    print("Type of questions:", type(data.get("questions")))
    print("Questions:", repr(data.get("questions"))[:200])
    print("Answers:", repr(data.get("answers")))
    print("Data keys:", data.keys())
