from flask import Flask, request, jsonify
from pythainlp.transliterate import romanize
import re

app = Flask(__name__)

# Hardcoded replacements (Thai to English words)
CUSTOM_REPLACEMENTS = {
    r"รีวิว": "review",
    r"ไดอารี": "diary",
    r"คิทเช่น": "kitchen",
    r"คาเฟ่": "cafe",
    r"บิวตี้": "beauty",
}

def preprocess(text):
    for pattern, replacement in CUSTOM_REPLACEMENTS.items():
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE | re.UNICODE)
    return text

def smart_romanize_with_preprocess(text):
    text = preprocess(text)
    words = re.split(r'(\s+|-)', text)
    out_words = []
    for word in words:
        if re.match(r'^[a-zA-Z0-9._-]+$', word):
            out_words.append(word)
        else:
            roman = romanize(word)
            roman_clean = re.sub(r'[-\s]+', '', roman)
            out_words.append(roman_clean if roman_clean else word)
    return "".join(out_words)

@app.route('/')
def home():
    return "✅ Thai karaoke romanization API running with hardcoded replacements!"

@app.route('/romanize', methods=['POST'])
def transliterate():
    data = request.get_json()
    text = data.get("text", "")
    result = smart_romanize_with_preprocess(text)
    return jsonify({"romanized": result})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
