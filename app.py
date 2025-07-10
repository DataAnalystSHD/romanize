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
    cleaned = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    print(f"🔤 After strip_fancy_unicode: '{cleaned}'", flush=True)
    return cleaned

def preprocess(text):
    text = strip_fancy_unicode(text)
    print(f"🔍 Before replacements: '{text}'", flush=True)
    for pattern, replacement in CUSTOM_REPLACEMENTS.items():
        if re.search(pattern, text, flags=re.IGNORECASE | re.UNICODE):
            print(f"✅ Replacing '{pattern}' with '{replacement}'", flush=True)
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE | re.UNICODE)
    print(f"✂️ After replacements: '{text}'", flush=True)
    return text

def smart_romanize_and_format(text):
    text = preprocess(text)
    words = re.split(r'(\s+|-)', text)
    print(f"🚀 Split words: {words}", flush=True)
    out_words = []
    for word in words:
        if re.match(r'^[a-zA-Z0-9._-]+$', word):
            print(f"🔠 Keeping ASCII word: '{word}'", flush=True)
            out_words.append(word)
        else:
            roman = romanize(word)
            roman_clean = re.sub(r'[-\s]+', '', roman)
            print(f"📝 Romanized '{word}' → '{roman_clean}'", flush=True)
            out_words.append(roman_clean if roman_clean else word)
    final = "".join(out_words)
    print(f"🧹 Before UTM cleanup: '{final}'", flush=True)
    final = re.sub(r'[^a-zA-Z0-9\s_-]', '', final)
    final = final.lower()
    final = re.sub(r'\s+', '-', final)
    print(f"✅ UTM formatted: '{final}'", flush=True)
    if not final.strip():
        fallback = re.sub(r'[^a-zA-Z0-9\s_-]', '', preprocess(text)).lower()
        fallback = re.sub(r'\s+', '-', fallback)
        print(f"⚠️ Fallback used: '{fallback}'", flush=True)
        final = fallback
    return final

@app.route('/')
def home():
    return "✅ Thai romanization UTM API with debug + flush!"

@app.route('/romanize', methods=['POST'])
def transliterate():
    data = request.get_json()
    text = data.get("text", "")
    print("\n============================", flush=True)
    print(f"🌟 New request for: '{text}'", flush=True)
    result = smart_romanize_and_format(text)
    print(f"✅ Final result: '{result}'", flush=True)
    print("============================\n", flush=True)
    return jsonify({"romanized": result})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
