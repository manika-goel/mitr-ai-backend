from flask import request, jsonify
from app.database import db
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import jwt
import os
from .chat_engine import get_mitrai_response
from app.toolkit_logic import get_toolkit_content
from app.chat_engine import get_mitrai_response
from app.toolkit_data import TOOLKIT_CONTENT

def setup_routes(app):

    # 1. SIGNUP: Normal (Email/Username based)
    @app.route('/api/signup/normal', methods=['POST'])
    def signup_normal():
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        # Basic Validation
        if password != confirm_password:
            return jsonify({"error": "Passwords do not match!"}), 400
        
        if db.users.find_one({"username": username, "auth_type": "normal"}):
            return jsonify({"error": "Username already taken!"}), 400

        # Password Hash karna security ke liye
        hashed_password = generate_password_hash(password)

        db.users.insert_one({
            "username": username,
            "password": hashed_password,
            "auth_type": "normal",
            "created_at": "timestamp" # Baad mein actual date daalenge
        })
        return jsonify({"message": "Normal Signup Successful!"}), 201

    # 2. SIGNUP: Anonymous (Nickname based)
    @app.route('/api/signup/anonymous', methods=['POST'])
    def signup_anonymous():
        data = request.get_json()
        nickname = data.get('nickname')
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        security_question = data.get('security_question')
        security_answer = data.get('security_answer')

        if password != confirm_password:
            return jsonify({"error": "Passwords do not match!"}), 400

        if db.users.find_one({"nickname": nickname, "auth_type": "anonymous"}):
            return jsonify({"error": "Nickname already exists!"}), 400

        hashed_password = generate_password_hash(password)

        db.users.insert_one({
            "nickname": nickname,
            "password": hashed_password,
            "security_question": security_question,
            "security_answer": security_answer.lower(),
            "auth_type": "anonymous"
        })
        return jsonify({"message": "Anonymous Signup Successful!"}), 201
    
    @app.route('/api/login/normal', methods=['POST'])
    def login_normal():
        data = request.get_json()
        user = db.users.find_one({"username": data.get('username'), "auth_type": "normal"})

        if user and check_password_hash(user['password'], data.get('password')):
            # Token generate ho raha hai
            token = jwt.encode({
                'user_id': str(user['_id']),
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
            }, os.getenv("SECRET_KEY"), algorithm="HS256")

            return jsonify({
                "message": "Login successful",
                "token": token,  # Ab response mein token jayega
                "username": user['username']
            }), 200
        return jsonify({"error": "Invalid credentials"}), 401

    @app.route('/api/login/anonymous', methods=['POST'])
    def login_anonymous():
        data = request.get_json()
        user = db.users.find_one({"nickname": data.get('nickname'), "auth_type": "anonymous"})

        if user and check_password_hash(user['password'], data.get('password')):
            # Anonymous token
            token = jwt.encode({
                'user_id': str(user['_id']),
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
            }, os.getenv("SECRET_KEY"), algorithm="HS256")

            return jsonify({
                "message": "Anonymous login successful",
                "token": token,
                "nickname": user['nickname']
            }), 200
        return jsonify({"error": "Invalid credentials"}), 401
    
    @app.route('/api/reset-password/normal', methods=['POST'])
    def reset_normal():
        data = request.get_json()
        username = data.get('username')
        new_password = data.get('new_password')

        user = db.users.find_one({"username": username, "auth_type": "normal"})
        if not user:
            return jsonify({"error": "User not found"}), 404

        hashed_pw = generate_password_hash(new_password)
        db.users.update_one({"username": username}, {"$set": {"password": hashed_pw}})
        
        return jsonify({"message": "Password reset successful!"}), 200

    @app.route('/api/reset-password/anonymous', methods=['POST'])
    def reset_anonymous():
        data = request.get_json()
        nickname = data.get('nickname')
        security_answer = data.get('security_answer')
        new_password = data.get('new_password')

        user = db.users.find_one({"nickname": nickname, "auth_type": "anonymous"})
        
        if not user:
            return jsonify({"error": "Anonymous user not found"}), 404

        # Security Answer match karna (Case-insensitive)
        if user.get('security_answer').lower() == security_answer.lower():
            hashed_pw = generate_password_hash(new_password)
            db.users.update_one({"nickname": nickname}, {"$set": {"password": hashed_pw}})
            return jsonify({"message": "Anonymous password reset successful!"}), 200
        else:
            return jsonify({"error": "Wrong security answer"}), 401
        
    @app.route('/api/user/update-language', methods=['POST'])
    def update_language():
        data = request.get_json()
        auth_type = data.get('auth_type') # 'normal' ya 'anonymous'
        language = data.get('language')   # 'hindi' ya 'english'
        
        # 1. Agar Normal User hai toh 'username' se dhundo
        if auth_type == 'normal':
            username = data.get('username')
            db.users.update_one({"username": username}, {"$set": {"language": language}})
        
        # 2. Agar Anonymous User hai toh 'nickname' se dhundo
        elif auth_type == 'anonymous':
            nickname = data.get('nickname')
            db.users.update_one({"nickname": nickname}, {"$set": {"language": language}})
        
        return jsonify({"message": f"Language updated to {language} successfully!"}), 200
    
    @app.route('/api/chat', methods=['POST'])
    def chat_with_mitr():
        try:
            data = request.json
            user_msg = data.get("message")
            user_id = data.get("user_id", "onboarding_user")
            
            # Aapka Gemini AI logic yahan rahega
            ai_reply = get_mitrai_response(user_msg) 

            stress_keywords = ["suicide", "depressed", "kill", "hopeless", "can't take it", "hurt myself", "panic", "anxiety"]

            stress_score = 0
            if any(word in user_msg for word in stress_keywords):
                stress_score = 90  # High stress detect hua
            else:
                stress_score = 30  # Normal stress
            # User ka message save karein
            db.chats.insert_one({
                "user_id": user_id,
                "text": user_msg,
                "sender": "user",
                "stress_level": stress_score,
                "timestamp": datetime.datetime.utcnow()
            })
            # Bot ka reply save karein
            db.chats.insert_one({
                "user_id": user_id,
                "text": ai_reply,
                "sender": "bot",
                "timestamp": datetime.datetime.utcnow()
            })

            return jsonify({"reply": ai_reply})
        except Exception as e:
                return jsonify({"error": str(e)}), 500
        
    @app.route('/api/toolkit/videos', methods=['GET'])
    def get_videos():
        data = get_toolkit_content('video')
        return jsonify(data)


    @app.route('/api/mood/initial-quiz', methods=['POST'])
    def save_initial_quiz():
        try:
            data = request.json.get('answers')
            if not data:
                return jsonify({"error": "No data received"}), 400

            # Mood ko points mein convert karne ka logic
            mapping = {
                "SAD": 1, "STRESSED": 1, "ANXIOUS": 2, "TIRED": 2,
                "NEUTRAL": 3, "OKAY": 3,
                "HAPPY": 4, "CALM": 4, "GOOD": 4,
                "EXCITED": 5, "GREAT": 5, "AMAZING": 5
            }

            total_score = 0
            count = 0
            for item in data:
                ans_label = str(item.get('answer', '')).upper()
                if ans_label in mapping:
                    total_score += mapping[ans_label]
                    count += 1

            # Average intensity nikalna
            final_intensity = round(total_score / count) if count > 0 else 3

            # Database mein save karna
            quiz_entry = {
                "user_id": "onboarding_user",
                "responses": data,
                "intensity": final_intensity,
                "is_initial": True,
                "timestamp": datetime.datetime.utcnow(),
                "date": datetime.datetime.utcnow().strftime('%Y-%m-%d') # Ye calendar ke liye zaruri hai
            }

            db.moods.insert_one(quiz_entry)
            return jsonify({"status": "success", "calculated_intensity": final_intensity}), 200

        except Exception as e:
            print(f"Quiz Save Error: {e}")
            return jsonify({"error": str(e)}), 500
        
        
    @app.route('/api/mood/analytics', methods=['GET'])
    def get_analytics():
        try:
            # 1. MongoDB se data fetch karein
            # 'onboarding_user' ki jagah dynamic user_id bhi use kar sakte hain
            all_moods = list(db.moods.find({"user_id": "onboarding_user"}).sort("timestamp", -1).limit(20))
            
            if not all_moods:
                return jsonify({
                    "avatar_state": "neutral", 
                    "latest_intensity": 3, 
                    "chart_data": []
                }), 200

            # 2. Latest data for Avatar
            latest = all_moods[0]
            latest_intensity = latest.get("intensity", 3)
            
            avatar_state = "neutral"
            if latest_intensity >= 4: 
                avatar_state = "happy"
            elif latest_intensity <= 2: 
                avatar_state = "stressed"

            # 3. Chart Data taiyaar karein (Purana grouping logic hata kar clean loop)
            chart_data = []
            # Reversed taaki graph left-to-right (purane se naya) chale
            for m in reversed(all_moods):
                # Check if timestamp exists to avoid crash
                ts = m.get("timestamp")
                day_label = ts.strftime("%d %b %H:%M") if ts else "N/A"
                
                chart_data.append({
                    "day": day_label, 
                    "mood": int(m.get("intensity", 3))
                })

            # Final single return jo pura data ek saath bhejega
            return jsonify({
                "avatar_state": avatar_state,
                "latest_intensity": int(latest_intensity),
                "chart_data": chart_data
            }), 200

        except Exception as e:
            print(f"Final Analytics Error: {e}")
            return jsonify({"error": str(e)}), 500
    
    @app.route('/api/chat/history/<user_id>', methods=['GET'])
    def get_chat_history(user_id):
        try:
        # User ki sari chats uthayein aur purani se nayi ke order mein lagayein
            history = list(db.chats.find({"user_id": user_id}).sort("timestamp", 1))
            print(f"Fetching history for: {user_id}")
            # MongoDB ke format ko JSON format mein badlein
            formatted_history = []
            for chat in history:
                formatted_history.append({
                    "text": chat.get("text", ""),
                    "sender": chat.get("sender", "bot")
                })
                
            return jsonify(formatted_history), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
        # Calendar events fetch karne ke liye
    @app.route('/api/calendar/<user_id>', methods=['GET'])
    def get_calendar_events(user_id):
        try:
            # Calendar ke liye data fetch
            mood_data = list(db.moods.find({"user_id": user_id}, {"_id": 0}))
            return jsonify(mood_data), 200
        except Exception as e:
            print(f"Calendar Fetch Error: {e}")
            return jsonify([]), 500 # Kuch galat hua toh khali list bhej do
        # Naya event save karne ke liye
    @app.route('/api/calendar/save', methods=['POST'])
    def save_calendar_event():
        try:
            data = request.json
            if not data.get('user_id') or not data.get('date'):
                return jsonify({"error": "Missing data"}), 400

            # Upsert logic: Agar usi din ka data hai toh update, nahi toh naya insert
            db.moods.update_one(
                {"user_id": data['user_id'], "date": data['date']},
                {"$set": {
                    "mood": data.get('mood'),
                    "score": data.get('score'),
                    "color": data.get('color'),
                    "timestamp": datetime.datetime.utcnow() # Real-time tracking ke liye
                }},
                upsert=True
            )
            return jsonify({"message": "Mood saved successfully!"}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
    @app.route('/api/counsellor/info', methods=['GET'])
    def counsellor_info():
        # Abhi ke liye aapki team ka details
        support_data = {
            "name": "MitrAI Support Expert",
            "availability": "24/7 Support",
            "contact_type": "WhatsApp / Call",
            "contact_value": "+91-9412619588",
            "message_template": "Hello Mitr, I need urgent support.",
            "bio": "Experienced in crisis management and mental well-being."
        }
        return jsonify(support_data), 200
        
        