from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import join_room, leave_room, send, SocketIO
import secrets
import string
from logic.game import Game


app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

rooms = {}
current_instruction = "Enter a word used to generate the start of the story"
# session["current_instruction"] = current_instruction
keywords = []

# Add this function to app.py
@socketio.on("start_game")
def start_game():
    print("Game started!!!")
    # room is room ID
    room = session.get("room")
    
    # Logic to start the game
    send({"name": "System", "message": "The game has started!"}, to=room)
    print(f"Game started in room {room}")

    # create a new game object
    game = Game(rooms[room]["members"])
    game.assign_aliases()



def generate_unique_room_id(length):
    characters = string.ascii_letters + string.digits
    while True:
        random_string = ''.join(secrets.choice(characters) for _ in range(length))
        
        if random_string not in rooms:
            return random_string

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
    return render_template("room.html", room_id=room, messages=rooms[room]["messages"], current_instruction=current_instruction)

@socketio.on("message")
def message(data):
    room = session.get("room")
    if room not in rooms:
        return redirect(url_for("index"))
    
    # current_instruction = session.get("current_instruction","")

    if current_instruction == "Enter a word used to generate the start of the story":
        keywords.append(data["data"])
        print(f"Keyword added: {data['data']}")

        # session["current_instruction"] = "Enter a sentence to continue the story"

        
    content = {
        "name": session.get("user_name"),
        "message": data["data"]
    }
    send(content, to=room)
    rooms[room]["messages"].append(content)
    print(f"{session.get('user_name')} said: {data['data']}")

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
    send({"name": user_name, "message": "has entered the room."}, to=room)
    rooms[room]["members"] += 1
    print(f"{user_name} joined room {room}")
    
@socketio.on("disconnect")
def disconnect():
    room = session.get("room")
    user_name = session.get("user_name")
    leave_room(room)

    if room in rooms:
        rooms[room]["members"] -= 1
        if rooms[room]["members"] <= 0:
            del rooms[room]
            
    send({"name": user_name, "message": "has left the room"}, to=room)
    print(f"{user_name} has left the room {room}")
    
if __name__ == "__main__":
    socketio.run(app, debug=True)