from flask import jsonify
from app.database import db # Aapka database instance yahan se aayega

def get_toolkit_content(content_type):
    try:
            # Database se us type ka content uthao (jaise 'video', 'activity', ya 'story')
            # Hum .limit(10) kar rahe hain taaki bohot saara data ek saath na aaye
            # Ye har baar database se random items uthayega
        content = list(db.toolkit.aggregate([{"$match": {"type": content_type}}, {"$sample": {"size": 4}}]))
            
        for item in content:
                item["_id"] = str(item["_id"]) # MongoDB ID ko frontend ke liye string mein badlo
                
        return content
    except Exception as e:
        print(f"Toolkit Logic Error: {e}")
        return []