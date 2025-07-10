from flask import Flask, request, jsonify
from pythainlp.transliterate import romanize

app = Flask(__name__)

@app.route('/romanize', methods=['POST'])
def transliterate():
    data = request.get_json()
    text = data.get("text", "")
    return jsonify({
        "romanized": romanize(text)
    })

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
