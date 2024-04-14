from flask import Flask, render_template, request, jsonify
from query_data import fetch_response

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/send", methods=['POST'])
def send():
    user_text = request.json['message']
    if not user_text:
        return jsonify(message="")

    response = fetch_response(user_text)
    return jsonify(message=response)


if __name__ == '__main__':
    app.run(debug=True, port=8080)
