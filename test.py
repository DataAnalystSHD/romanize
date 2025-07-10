import requests

def test_romanize(text):
    response = requests.post("http://localhost:8080/romanize", json={"text": text})
    if response.status_code == 200:
        print(f"✅ Input: {text}")
        print(f"➡️  Romanized: {response.json()['romanized']}")
    else:
        print("❌ Failed:", response.text)

if __name__ == "__main__":
    test_romanize("แฟรรี่รีวิว")
    test_romanize("รีวิวคาเฟ่")
    test_romanize("ไดอารีของฉัน")
    test_romanize("สำ นั ก ป้ า ย ย า")
    test_romanize("𝙆𝙖𝙧𝙣 𝙎𝙩𝙤𝙧𝙮 ; บ้านของกาญจน์")
