from flask import Flask, request, jsonify
from thai2rom import thai2rom
import unicodedata
import re

app = Flask(__name__)

# 🔥 Hard-coded common Thai replacements
CUSTOM_REPLACEMENTS = {
    "ไดอารี": "diary",
    "รีวิว": "review",
    "คิทเช่น": "kitchen",
    "คาเฟ่": "cafe",
    "บิวตี้": "beauty",
    # you can add more as you analyze your data
}

def strip_fancy_unicode(text):
    """
    Convert stylized unicode (𝙎𝙩𝙤𝙧𝙮, etc) to plain ASCII.
    """
    return unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")

def preprocess_custom(text):
    """
    Replace common Thai marketing words with direct English equivalents.
    """
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

    text = strip_fancy_unicode(text)  # 🔥 normalize fancy fonts
    text = preprocess_custom(text)    # 🔥 direct replacements

    romanized = thai2rom(text)        # karaoke transliteration
    romanized_clean = romanized.replace("-", "")  # no hyphens for UTM

    return jsonify({
        "romanized": romanized_clean
    })

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
