from pymongo import MongoClient
import os
from dotenv import load_dotenv

# .env file se variables load karne ke liye
load_dotenv()

def get_db():
    try:
        # URI ko .env se uthayenge
        uri = os.getenv("MONGO_URI")
        client = MongoClient(uri)
        
        # Database ka naam 'mitrai_db'
        db = client.get_database()
        
        print("✅ MongoDB Connected Successfully!")
        return db
    except Exception as e:
        print(f"❌ Database connection error: {e}")
        return None

# Database instance jo hum baaki files mein use karenge
db = get_db()