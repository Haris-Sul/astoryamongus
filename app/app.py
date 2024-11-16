from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO
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
        room_name = request.form.get("room_name")
        create = request.form.get("create", False)
        room_id = request.form.get("room_id")
        join = request.form.get("join", False)
        
        if not room_name:
            return render_template("index.html", error="Please enter a room name.", room_id=room_id, room_name=room_name)
        
        if join != False and not room_id:
            return render_template("index.html", error="Please enter a room ID.", room_id=room_id, room_name=room_name)
        
        room = room_id
        # If you are creating a room (create button is pressed)
        if create != False:
            room = generate_unique_room_id(5)
            rooms[room] = {"members": 0, "messages": []}
        # Otherwise, you are joining a room. If room does not exist with that ID.
        elif room_id not in rooms:
            return render_template("index.html", error="Room does not exist.", room_id=room_id, room_name=room_name)
            
        session["room"] = room
        session["room_name"] = room_name
        
        return redirect(url_for("room"))
        
    return render_template("index.html")

@app.route("/room")
def room():
    room = session.get("room")
    if room is None or session.get("name") is None or room not in rooms:
        return redirect(url_for("index"))
    return render_template("room.html")

if __name__ == "__main__":
    socketio.run(app, debug=True)