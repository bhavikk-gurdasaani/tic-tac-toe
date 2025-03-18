from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Initialize empty board
board = [[" " for _ in range(3)] for _ in range(3)]
players = ["X", "O"]
turn = 0

def check_winner():
    # Check rows and columns
    for i in range(3):
        if all(board[i][j] == players[turn % 2] for j in range(3)) or all(board[j][i] == players[turn % 2] for j in range(3)):
            return True
    # Check diagonals
    if all(board[i][i] == players[turn % 2] for i in range(3)) or all(board[i][2 - i] == players[turn % 2] for i in range(3)):
        return True
    return False

@app.route("/")
def index():
    return render_template("index.html", board=board)

@app.route("/move", methods=["POST"])
def move():
    global turn
    data = request.get_json()
    row, col = int(data["row"]), int(data["col"])

    if board[row][col] == " ":
        board[row][col] = players[turn % 2]
        if check_winner():
            return jsonify({"winner": players[turn % 2], "board": board})
        turn += 1
        return jsonify({"board": board})
    return jsonify({"error": "Invalid move"}), 400

@app.route("/reset", methods=["POST"])
def reset():
    global board, turn
    board = [[" " for _ in range(3)] for _ in range(3)]
    turn = 0
    return jsonify({"board": board})

if __name__ == "__main__":
    app.run(debug=True)
