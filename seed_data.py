from app.database import db
from app.models import ToolkitItem

def seed_toolkit():
    # Purana data saaf karte hain taaki fresh start ho
    db.toolkit.delete_many({})
    
    sample_data = [
        # --- VIDEOS ---
        ToolkitItem("Box Breathing Exercise", "video", "breathing", "https://www.youtube.com/watch?v=tEmt1ZnuxAk", "Stress kam karne ke liye 4 minute ki technique."),
        ToolkitItem("Mental Stress Booster", "video", "motivation", "https://www.youtube.com/watch?v=s5Zf5H-nNqQ", "Positive mindset ke liye tips."),
        ToolkitItem("Calming Mantra", "video", "mantra", "https://www.youtube.com/watch?v=mID7yV8t8fE", "Peaceful mantra for meditation."),

        # --- ACTIVITIES ---
        ToolkitItem("Digital Doodle Pad", "activity", "doodle", "https://quickdraw.withgoogle.com/", "Apne emotions ko draw karke express karein."),
        ToolkitItem("Coloring Book", "activity", "drawing", "https://www.google.com/logos/2020/kits/coloring/index.html", "Mindful coloring activity."),
        ToolkitItem("Music Therapy", "activity", "music", "https://musiclab.chromeexperiments.com/Song-Maker/", "Apna khud ka sukoon bhara music banayein."),

        # --- STORIES ---
        ToolkitItem("The Power of Calm", "story", "spiritual", "Ek baar ek raja bohot pareshan tha...", "Ek kahani jo batati hai ki shanti bahar nahi, andar hoti hai."),
        ToolkitItem("A Small Step Every Day", "story", "motivational", "Ek nanhi chinti ne pahaad chadhne ka faisla kiya...", "Consitency ki taqat par ek choti si kahani."),
        ToolkitItem("Buddha and the Angry Man", "story", "spiritual", "Jab ek vyakti ne Buddha ko bura-bhala kaha...", "Gusse ko handle karne ki ek purani seekh.")
    ]

    for item in sample_data:
        db.toolkit.insert_one(item.to_dict())

    print("✅ Toolkit Data (Videos, Activities, Stories) Seed ho gaya hai!")

if __name__ == "__main__":
    seed_toolkit()

#from app.database import db

def get_toolkit_content(content_type):
    try:
        # MongoDB ka $sample operator har baar random data pick karega
        # Isse user ko har baar naya content dikhega
        pipeline = [
            {"$match": {"type": content_type}},
            {"$sample": {"size": 6}} # Har baar 6 random items uthayega
        ]
        
        content = list(db.toolkit.aggregate(pipeline))
        
        for item in content:
            item["_id"] = str(item["_id"]) 
            
        return content
    except Exception as e:
        print(f"Toolkit Logic Error: {e}")
        return []