from flask import Flask, request, jsonify
from pythainlp.transliterate import romanize
import unicodedata
import re

app = Flask(__name__)

CUSTOM_REPLACEMENTS = {
    r"รีวิว": "review",
    r"ไดอารี": "diary",
    r"คิทเช่น": "kitchen",
    r"คาเฟ่": "cafe",
    r"บิวตี้": "beauty",
}

def strip_fancy_unicode(text):
    # Convert fancy unicode fonts to plain ASCII
    return unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")

def preprocess(text):
    text = strip_fancy_unicode(text)
    for pattern, replacement in CUSTOM_REPLACEMENTS.items():
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE | re.UNICODE)
    return text

def smart_romanize_and_format(text):
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
    final = "".join(out_words)
    # Remove any character not a-z, 0-9, space, underscore, hyphen
    final = re.sub(r'[^a-zA-Z0-9\s_-]', '', final)
    final = final.lower()
    final = re.sub(r'\s+', '-', final)
    return final

@app.route('/')
def home():
    return "✅ Thai karaoke romanization API ready for clean UTM!"

@app.route('/romanize', methods=['POST'])
def transliterate():
    data = request.get_json()
    text = data.get("text", "")
    result = smart_romanize_and_format(text)
    return jsonify({"romanized": result})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
