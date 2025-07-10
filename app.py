from flask import Flask, request, jsonify
from thai2rom import thai2rom
import unicodedata
import re

app = Flask(__name__)

# 🔥 Hard-coded common Thai words to English
CUSTOM_REPLACEMENTS = {
    "ไดอารี": "diary",
    "รีวิว": "review",
    "คิทเช่น": "kitchen",
    "คาเฟ่": "cafe",
    "บิวตี้": "beauty",
    "บ้าน": "ban",  # example partial if you want
    # add more as needed
}

def strip_fancy_unicode(text):
    """
    Turn fancy fonts like 𝙆𝙖𝙧𝙣 to Karn.
    """
    return unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")

def preprocess_custom(text):
    """
    Replace common marketing words inside any string.
    """
    for thai_word, english_word in CUSTOM_REPLACEMENTS.items():
        text = re.sub(thai_word, english_word, text, flags=re.IGNORECASE | re.UNICODE)
    return text

def smart_transliterate(text):
    words = re.split(r'(\s+|-)')  # keep spaces/hyphens to break on them
    new_words = []
    for word in words:
        if re.match(r'^[a-zA-Z0-9._-]+$', word):
            new_words.append(word)
        else:
            cleaned = strip_fancy_unicode(word)
            cleaned = preprocess_custom(cleaned)
            roman = thai2rom(cleaned)
            roman = re.sub(r'[-\s]+', '', roman)  # remove hyphens & spaces
            new_words.append(roman)
    return "".join(new_words)

@app.route('/')
def home():
    return "✅ Thai karaoke romanization API is running!"

@app.route('/romanize', methods=['POST'])
def transliterate():
    data = request.get_json()
    text = data.get("text", "")
    text = preprocess_custom(text)  # ensure forced words replaced first
    result = smart_transliterate(text)
    return jsonify({"romanized": result})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
