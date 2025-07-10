from flask import Flask, request, jsonify
from pythainlp.transliterate import romanize
import re

app = Flask(__name__)

# Full custom replacements (as regex -> replacement)
CUSTOM_REPLACEMENTS = {
    r"รี.?วิ": "review",
    r"ไดอารี": "diary",
    r"คิทเช่น": "kitchen",
    r"คาเฟ่": "cafe",
    r"บิวตี้": "beauty",
}

def preprocess(text):
    for pattern, replacement in CUSTOM_REPLACEMENTS.items():
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE | re.UNICODE)
    return text

@app.route('/romanize', methods=['POST'])
def transliterate():
    data = request.get_json()
    text = data.get("text", "")
    text = preprocess(text)
    result = romanize(text)
    return jsonify({"romanized": result})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
