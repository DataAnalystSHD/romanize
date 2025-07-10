from flask import Flask, request, jsonify
from thai2rom import thai2rom
import re

app = Flask(__name__)

# 📝 common Thai words that should become English directly
CUSTOM_REPLACEMENTS = {
    "ไดอารี": "diary",
    "รีวิว": "review",
    "คิทเช่น": "kitchen",
    "คาเฟ่": "cafe",
    "บิวตี้": "beauty",
    # add more as you find them
}

def preprocess_custom(text):
    # use regex to replace all occurrences of each key
    for thai_word, english_word in CUSTOM_REPLACEMENTS.items():
        text = re.sub(thai_word, english_word, text)
    return text

@app.route('/')
def home():
    return "Thai karaoke romanization service running!"

@app.route('/romanize', methods=['POST'])
def transliterate():
    data = request.get_json()
    text = data.get("text", "")
    text = preprocess_custom(text)  # 🔥 apply forced replacements
    romanized = thai2rom(text)
    romanized_clean = romanized.replace("-", "")
    return jsonify({
        "romanized": romanized_clean
    })

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
