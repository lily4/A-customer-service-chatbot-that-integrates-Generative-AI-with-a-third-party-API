from flask import Flask, request, jsonify, render_template
from chatbot import handle_message

app = Flask(__name__)


@app.route("/")
def home():
    """
    Serve the web chat UI.
    Expects templates/chat.html to exist.
    """
    return render_template("chat.html")


@app.route("/chat", methods=["POST"])
def chat():
    """
    Chat endpoint.
    Expects JSON: { "message": "..." }
    Returns JSON: { "reply": "..." }
    """
    data = request.get_json(force=True)
    user_message = data.get("message", "")

    reply = handle_message(user_message)

    return jsonify({"reply": reply})


if __name__ == "__main__":
    # host=0.0.0.0 so it works in Codespaces
    app.run(host="0.0.0.0", port=5000)
