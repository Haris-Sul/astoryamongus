from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Sample data
story_prompt = "Once upon a time..."
players = ["Alice", "Bob", "Charlie"]


@app.route("/")
def index():
    return render_template("index.html", story_prompt=story_prompt, players=players)


@app.route("/create_room", methods=["POST"])
def create_room():
    room_name = request.form["room_name"]
    # Logic to create a room
    return redirect(url_for("home"))


@app.route("/join_room", methods=["POST"])
def join_room():
    room_name = request.form["room_name"]
    # Logic to join a room
    return redirect(url_for("home"))


@app.route("/submit_sentence", methods=["POST"])
def submit_sentence():
    user_sentence = request.form["user_sentence"]
    # Logic to handle the submitted sentence
    return redirect(url_for("home"))


@app.route("/submit_vote", methods=["POST"])
def submit_vote():
    player_vote = request.form["player_vote"]
    # Logic to handle the vote
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
