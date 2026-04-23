from flask import Flask, request, jsonify

app = Flask(__name__)

# База данных пользователей
users = {
    "676767": {
        "id": "676767", "nick": "OWNER", "balance": 1000000, 
        "premium": True, "emoji": "👑", "color": "#FFD700"
    }
}
next_user_id = 2

@app.route('/')
def home():
    return "Сервер мессенджера запущен!"

@app.route('/register', methods=['POST'])
def register():
    global next_user_id
    data = request.json
    nick = data.get('nick', 'NewUser')[:30]
    email = data.get('email', '')
    new_id = str(next_user_id).zfill(6)
    users[new_id] = {
        "id": new_id, "nick": nick, "email": email,
        "balance": 0, "premium": False, "emoji": "", "color": "#FFFFFF"
    }
    next_user_id += 1
    return jsonify({"status": "success", "id": new_id})

@app.route('/admin', methods=['POST'])
def admin():
    data = request.json
    if data.get('admin_id') != "676767":
        return jsonify({"error": "No access"}), 403
    target = data.get('target_id')
    if target in users:
        users[target]['balance'] += int(data.get('add_cash', 0))
        return jsonify({"status": "success"})
    return jsonify({"error": "Not found"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
