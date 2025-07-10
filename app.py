from flask import Flask, request, jsonify
from thai2rom import thai2rom

app = Flask(__name__)

@app.route('/')
def home():
    return "Thai karaoke romanization service running!"

@app.route('/romanize', methods=['POST'])
def transliterate():
    data = request.get_json()
    text = data.get("text", "")
    romanized = thai2rom(text)
    romanized_clean = romanized.replace("-", "")  # ✅ remove dashes
    return jsonify({
        "romanized": romanized_clean
    })

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
