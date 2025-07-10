from flask import Flask, request, jsonify
from thai2rom import thai2rom
import unicodedata
import re

app = Flask(__name__)

# 🔥 Your forced replacements
CUSTOM_REPLACEMENTS = {
    "ไดอารี": "diary",
    "รีวิว": "review",
    "คิทเช่น": "kitchen",
    "คาเฟ่": "cafe",
    "บิวตี้": "beauty",
    # add more as needed
}

def strip_fancy_unicode(text):
    """
    Convert fancy unicode (𝙆𝙖𝙧𝙣 𝙎𝙩𝙤𝙧𝙮) to plain ascii (Karn Story)
    """
    return unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")

def preprocess_custom(text):
    """
    Replace known Thai words anywhere in string with direct English equivalent.
    """
    for thai_word, english_word in CUSTOM_REPLACEMENTS.items():
        text = re.sub(thai_word, english_word, text, flags=re.IGNORECASE | re.UNICODE)
    return text

def smart_transliterate(text):
    """
    Strip fancy fonts, apply custom replacements, then only romanize Thai fragments.
    """
    text = strip_fancy_unicode(text)
    text = preprocess_custom(text)

    words = re.split(r'(\s+|-)')  # keep spaces and hyphens as separators
    new_words = []
    for word in words:
        if re.match(r'^[a-zA-Z0-9._-]+$', word):
            new_words.append(word)
        else:
            roman = thai2rom(word)
            roman = re.sub(r'[-\s]+', '', roman)  # remove hyphens and spaces
            new_words.append(roman)
    return "".join(new_words)

@app.route('/')
def home():
    return "✅ Thai karaoke romanization API running!"

@app.route('/romanize', methods=['POST'])
def transliterate():
    data = request.get_json()
    text = data.get("text", "")
    result = smart_transliterate(text)
    return jsonify({"romanized": result})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
