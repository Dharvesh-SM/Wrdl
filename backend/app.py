from flask import Flask, jsonify, request
from flask_cors import CORS
import random

TARGET_WORD = None

app = Flask(__name__)
CORS(app)

WORDS = [
    "about", "above", "actor", "acute", "admit", "adult", "after", "again", "agent", "agree",
    "ahead", "aisle", "alert", "alive", "allow", "alone", "along", "alter", "among", "angle",
    "anger", "angry", "ankle", "apart", "apply", "arena", "argue", "arise", "array", "aside",
    "asset", "atlas", "attic", "audio", "audit", "avoid", "await", "award", "aware", "awful",
    "basic", "basis", "beach", "begin", "being", "below", "bench", "birth", "black", "blade",
    "blame", "blank", "blast", "blend", "blind", "block", "blood", "board", "boost", "booth",
    "bound", "brain", "brand", "brave", "bread", "break", "brief", "bring", "broad", "brown",
    "build", "bunch", "burst", "buyer", "cable", "cadre", "carry", "catch", "cause", "cease",
    "chain", "chair", "chart", "chase", "cheap", "check", "chest", "chief", "child", "china",
    "claim", "class", "clean", "clear", "clerk", "clock", "close", "cloud", "coach", "coast",
    "color", "comic", "count", "court", "cover", "craft", "crash", "cream", "crime", "cross",
    "crowd", "curve", "cycle", "daily", "dance", "dated", "deals", "death", "debut", "delay",
    "depth", "diary", "dirty", "disco", "ditch", "doubt", "draft", "drain", "drama", "dream",
    "dress", "drink", "drive", "dying", "early", "earth", "eight", "elite", "empty", "enemy",
    "enjoy", "enter", "entry", "equal", "error", "event", "every", "exact", "exist", "extra",
    "faced", "faces", "facts", "fails", "faith", "false", "fancy", "fault", "favor", "fears",
    "field", "fifth", "fifty", "fight", "final", "finds", "fired", "first", "fixed", "flags",
    "flash", "fleet", "floor", "flows", "fluid", "focus", "force", "forth", "forty", "forum",
    "found", "frame", "frank", "fraud", "fresh", "front", "fruit", "fully", "funny", "giant",
    "given", "glass", "globe", "going", "grace", "grade", "grand", "grant", "grass", "great",
    "green", "guard", "guess", "guest", "guide", "habit", "happy", "heart", "heavy", "hello"
]

@app.route('/word', methods = ['GET'])
def get_word():
    global TARGET_WORD
    TARGET_WORD = random.choice(WORDS)
    print(f"New target word: {TARGET_WORD}")
    return jsonify({"word": TARGET_WORD})

@app.route('/check', methods = ['POST'])
def check_word():
    global TARGET_WORD
    data = request.get_json()
    guessed_word = data.get("word", "").lower()

    if len(guessed_word) != len(TARGET_WORD):
        return jsonify({"valid": False, "message": "Invalid length!"})

    if guessed_word == TARGET_WORD:
        return jsonify({"valid": True, "message": "Correct word!", "hints": ["🟩"] * len(TARGET_WORD)})

    hints = []
    target_word_list = list(TARGET_WORD)


    for i in range(len(guessed_word)):
        if guessed_word[i] == TARGET_WORD[i]:
            hints.append("🟩")
            target_word_list[i] = None  
        else:
            hints.append(None)


    for i in range(len(guessed_word)):
        if hints[i] is None:
            if guessed_word[i] in target_word_list:
                hints[i] = "🟨"
                target_word_list[target_word_list.index(guessed_word[i])] = None
            else:
                hints[i] = "⬜️"

    return jsonify({"valid": False, "message": "Try again!", "hints": hints})

@app.route('/restart', methods=['GET'])
def restart_game():
    """Resets the target word and restarts the game"""
    global TARGET_WORD
    TARGET_WORD = random.choice(WORDS)
    print(f"Game restarted! New word: {TARGET_WORD}") 
    return jsonify({"message": "Game restarted!", "word": TARGET_WORD})


if __name__ == '__main__':
    app.run(debug=True)