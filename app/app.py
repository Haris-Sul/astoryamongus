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


# Add this function to app.py
@socketio.on("setup_game")
def setup_game():
    print("Game started!!!")
    # room is room ID
    room = session.get("room")
    
    # Logic to start the game
    send({"name": "System", "message": "The game has started!"}, to=room)
    print(f"Game started in room {room}")

    # create a new game object
    game = Game(rooms[room]["members"])
    game.assign_aliases()

    # add the data to the room
    rooms[room]["current_instruction"] = "Enter a word used to generate the start of the story"
    rooms[room]["game"] = game
    rooms[room]["keywords"] = []
    
    
    socketio.emit("update_instruction", {"current_instruction": rooms[room]["current_instruction"]}, to=room)
    print(rooms)
    

def start_game():
    room = session.get("room")
    rooms[room]["started"] = True
    game = rooms[room]["game"]

    print(rooms[room])
    game.generate_initial_story(rooms[room]["keywords"])

    content = {
        "name": "Story",
        "message": game.story.story_text
    }
    send(content, to=room)
    # enable the first  player to take their turn
    # check if this player is the current player
    print(game.players[game.current_player].name)
    print(game.players[game.current_player].is_ai)

    if game.players[game.current_player].is_ai:

        content = {
        "name": "Story",
        "message": game.ai_turn()
        }
        send(content, to=room)

    print(game.current_player)
    if game.current_player == session["id"]:
        socketio.emit("your_turn", to=room)
    # else:
    #     # if so, emit a message to the room to let them know it is their turn
    #     # socketio.emit("not_your_turn", {"current_instruction": rooms[room]["current_instruction"]}, to=room
    #     socketio.emit("not_your_turn", to=room)




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
            rooms[room]["current_instruction"] = "Enter a word used to generate the start of the story"
        # Otherwise, you are joining a room. If room does not exist with that ID.
        elif room_id not in rooms:
            return render_template("index.html", error="Room does not exist.", room_id=room_id, user_name=user_name, current_instruction=rooms[room]["current_instruction"])
            
        session["room"] = room
        session["user_name"] = user_name
        
        return redirect(url_for("room"))
        
    return render_template("index.html")

@app.route("/room")
def room():
    room = session.get("room")
    if room is None or session.get("user_name") is None or room not in rooms:
        return redirect(url_for("index"))
    
    # session["current_instruction"] = current_instruction
    return render_template("room.html", room_id=room, messages=rooms[room]["messages"], current_instruction=rooms[room]["current_instruction"])

@socketio.on("message")
def message(data):
    room = session.get("room")
    if room not in rooms:
        return redirect(url_for("index"))
    
    if rooms[room]["current_instruction"] == "Enter a word used to generate the start of the story":
        rooms[room]["keywords"].append(data["data"])
        print(f"Keyword added: {data['data']}")


        if len(rooms[room]["keywords"]) == rooms[room]["members"]:
            rooms[room]["current_instruction"] = "Enter a sentence to continue the story"
            # session["current_instruction"] = current_instruction
            start_game()

    elif rooms[room]["current_instruction"] == "Enter a sentence to continue the story":

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
    session["id"] = rooms[room]["members"] #0 based matches index in game object
    rooms[room]["members"] += 1
    rooms[room]["started"] = False
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