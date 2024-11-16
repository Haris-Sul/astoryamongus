from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import join_room, leave_room, send, SocketIO
import secrets
import string

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

rooms = {}

def generate_unique_room_id(length):
    characters = string.ascii_letters + string.digits
    for _ in range(length):
        secure_random_string = ''.join(secrets.choice(characters))
    
    return secure_random_string
        
@app.route("/", methods=["POST", "GET"])
def index():
    session.clear()
    if request.method == "POST":
        user_name = request.form.get("user_name")
        create = request.form.get("create", False)
        room_id = request.form.get("room_id")
        join = request.form.get("join", False)
        
        if not user_name:
            return render_template("index.html", error="Please enter a user name.", room_id=room_id, user_name=user_name)
        
        if join != False and not room_id:
            return render_template("index.html", error="Please enter a room ID.", room_id=room_id, user_name=user_name)
        
        room = room_id
        # If you are creating a room (create button is pressed)
        if create != False:
            room = generate_unique_room_id(5)
            rooms[room] = {"members": 0, "messages": []}
        # Otherwise, you are joining a room. If room does not exist with that ID.
        elif room_id not in rooms:
            return render_template("index.html", error="Room does not exist.", room_id=room_id, user_name=user_name)
            
        session["room"] = room
        session["user_name"] = user_name
        
        return redirect(url_for("room"))
        
    return render_template("index.html")

@app.route("/room")
def room():
    room = session.get("room")
    if room is None or session.get("user_name") is None or room not in rooms:
        return redirect(url_for("index"))
    return render_template("room.html")

@socketio.on("connect")
def connect(auth):
    room = session.get("room")
    user_name = session.get("user_name")
    
    if not room or not user_name:
        return
    if room not in rooms:
        leave_room(room)
        return
    
    join_room(room)
    send({"name": user_name, "message": " has entered the room."}, to=room)
    rooms[room]["members"] += 1
    print(f"{user_name} joined room {room}")

if __name__ == "__main__":
    socketio.run(app, debug=True)