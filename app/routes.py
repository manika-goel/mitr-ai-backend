from flask import request, jsonify
from app.database import db
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import jwt
import os
<<<<<<< HEAD
from .chat_engine import get_mitrai_response
from app.toolkit_logic import get_toolkit_content
from app.chat_engine import get_mitrai_response
from app.toolkit_data import TOOLKIT_CONTENT
=======
>>>>>>> a7f3e2a3acea6b4d2950f6b45f04e1cd6bb38f8b

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
        
<<<<<<< HEAD
        return jsonify({"message": f"Language updated to {language} successfully!"}), 200
    
    @app.route('/api/chat', methods=['POST'])
    def chat_with_mitr():
        data = request.json
        user_msg = data.get("message")
        
        if not user_msg:
            return jsonify({"error": "Message is empty"}), 400
            
        # Gemini se reply lein
        ai_reply = get_mitrai_response(user_msg)
        
        return jsonify({
            "reply": ai_reply,
            "sender": "MitrAI"
        })
    @app.route('/api/toolkit/videos', methods=['GET'])
    def get_videos():
        data = get_toolkit_content('video')
        return jsonify(data)

    @app.route('/api/toolkit/activities', methods=['GET'])
    def get_activities():
        data = get_toolkit_content('activity')
        return jsonify(data)

    @app.route('/api/toolkit/stories', methods=['GET'])
    def get_stories():
        data = get_toolkit_content('story')
        return jsonify(data)
    
    @app.route('/api/mood/initial-quiz', methods=['POST'])
    def save_initial_quiz():
        try:
            data = request.json.get('answers')
            if not data:
                return jsonify({"error": "No data received"}), 400

            # Behtar Mapping: 4 aur 5 wale options "Happy" banayenge
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

            # Average Score nikalna
            final_intensity = round(total_score / count) if count > 0 else 3

            quiz_entry = {
                "user_id": "onboarding_user",
                "responses": data,
                "intensity": final_intensity,
                "is_initial": True,
                "timestamp": datetime.datetime.utcnow() 
            }

            db.moods.insert_one(quiz_entry)
            return jsonify({"status": "success", "calculated_intensity": final_intensity}), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
    @app.route('/api/mood/analytics', methods=['GET'])
    def get_analytics():
        try:
            # Hamesha sabse latest (sabse naya) data uthayein
            latest_entry = db.moods.find({"user_id": "onboarding_user"}).sort("timestamp", -1).limit(1)
            
            mood_list = list(latest_entry)
            if not mood_list:
                return jsonify({"avatar_state": "neutral", "chart_data": []}), 200

            entry = mood_list[0]
            latest_intensity = entry.get("intensity", 3)

            # Avatar state decide karein
            avatar_state = "happy"
            if latest_intensity <= 2: avatar_state = "stressed"
            elif latest_intensity == 3: avatar_state = "neutral"

            return jsonify({
                "avatar_state": avatar_state,
                "latest_intensity": latest_intensity
            }), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @app.route('/api/toolkit/<mood>', methods=['GET'])
    def get_toolkit(mood):
    
        selected_content = TOOLKIT_CONTENT.get(mood.lower(), TOOLKIT_CONTENT['neutral'])

    # Frontend ko exactly ye structure chahiye taaki error na aaye
        response_data = {
            "videos": selected_content.get("videos", []),
            "activities": selected_content.get("activities", []),
            "stories": selected_content.get("stories", {
                "romance": [], "comedy": [], "suspense": [], "wisdom": []
            })
        }
    
        return jsonify(response_data), 200
    
    '''@app.route('/api/mood/analytics', methods=['GET'])
    def get_analytics():
        # TEST: Bina kisi calculation ke direct 'happy' bhej kar dekhte hain
        return jsonify({
            "avatar_state": "happy", 
            "latest_intensity": 5
        }), 200'''
=======
        return jsonify({"message": f"Language updated to {language} successfully!"}), 200
>>>>>>> a7f3e2a3acea6b4d2950f6b45f04e1cd6bb38f8b
