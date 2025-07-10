from flask import Flask, request, jsonify
from pythainlp.transliterate import romanize
import unicodedata
import re

app = Flask(__name__)

CUSTOM_REPLACEMENTS = {
    r"รีวิว": "review",
    r"รี.?วิ": "review",
    r"ไดอารี": "diary",
    r"คิทเช่น": "kitchen",
    r"คาเฟ่": "cafe",
    r"บิวตี้": "beauty",
}

def strip_fancy_unicode(text):
    cleaned = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    print(f"🔤 After strip_fancy_unicode: {cleaned}")
    return cleaned

def preprocess_custom(text):
    text = unicodedata.normalize("NFC", text)
    print(f"🔍 Before replacements (normalized NFC): {text}")
    for pattern, english_word in CUSTOM_REPLACEMENTS.items():
        if re.search(pattern, text, flags=re.IGNORECASE | re.UNICODE):
            print(f"✅ Matched pattern '{pattern}' -> replacing with '{english_word}'")
        text = re.sub(pattern, english_word, text, flags=re.IGNORECASE | re.UNICODE)
    print(f"✂️ After replacements: {text}")
    return text

def smart_transliterate(text):
    text = unicodedata.normalize("NFC", text)
    print(f"➡️ Raw input: {text}")
    text = strip_fancy_unicode(text)
    text = preprocess_custom(text)

    words = re.split(r'(\s+|-)')
    new_words = []
    for word in words:
        if re.match(r'^[a-zA-Z0-9._-]+$', word):
            print(f"🔠 Keeping ASCII word: {word}")
            new_words.append(word)
        else:
            roman = romanize(word)
            roman_clean = re.sub(r'[-\s]+', '', roman)
            print(f"📝 Romanized '{word}' to '{roman_clean}'")
            new_words.append(roman_clean)
    final_result = "".join(new_words)
    print(f"🚀 Final output: {final_result}")
    return final_result

@app.route('/')
def home():
    return "✅ Thai karaoke romanization API running with debug!"

@app.route('/romanize', methods=['POST'])
def transliterate():
    data = request.get_json()
    text = data.get("text", "")
    print("\n============================")
    print(f"🌟 New request for: {text}")
    result = smart_transliterate(text)
    print(f"✅ Final romanized result: {result}")
    print("============================\n")
    return jsonify({"romanized": result})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
