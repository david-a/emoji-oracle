import os
from flask import Flask, render_template, jsonify, request
from dotenv import load_dotenv
import openai
import random

# Load environment variables
load_dotenv()

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

# רשימת האימוג'ים לשימוש
ALL_EMOJIS = [
    "🌟",
    "🌙",
    "🌞",
    "🌈",
    "🌊",
    "🔮",
    "🎭",
    "🎪",
    "🎨",
    "🎯",
    "🎲",
    "🎰",
    "🃏",
    "🎴",
    "🎭",
    "🌸",
    "🍀",
    "🌺",
    "🌹",
    "🌷",
    "🌻",
    "🌼",
    "🍁",
    "🍂",
    "🍃",
    "🌴",
    "🌵",
    "🌾",
    "🌿",
    "☘️",
    "🍄",
    "🌰",
    "🦋",
    "🐌",
    "🐛",
    "🐜",
    "🐝",
    "🐞",
    "🦗",
    "🕷️",
    "🦂",
    "🦟",
    "🦠",
    "🧬",
    "🔬",
    "🔭",
    "📡",
    "💡",
    "🔋",
    "⚡️",
    "🌍",
    "🌎",
    "🌏",
    "🌐",
    "🗺️",
    "🗾",
    "🧭",
    "🏔️",
    "⛰️",
    "🌋",
    "🗻",
    "🏕️",
    "🏖️",
    "🏜️",
    "🏝️",
    "🏞️",
    "🏟️",
    "🏛️",
    "🏗️",
    "🧱",
    "🏘️",
    "🏚️",
    "🏠",
    "🏡",
    "🏢",
    "🏣",
    "🏤",
    "🏥",
    "🏦",
    "🏨",
    "🏩",
    "🏪",
    "🏫",
    "🏬",
    "🏭",
    "🏯",
    "🏰",
    "💒",
    "🗼",
    "🗽",
    "⛪️",
    "🕌",
    "🕍",
    "⛩️",
    "🕋",
    "⛲️",
    "⛺️",
    "🌁",
    "🌃",
    "🏙️",
    "🌄",
    "🌅",
    "🌆",
    "🌇",
    "🌉",
    "♨️",
    "🎠",
    "🎡",
    "🎢",
    "💈",
    "🎪",
]


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/generate-emojis")
def generate_emojis():
    # יצירת שלוש קבוצות של שלושה אימוג'ים
    emoji_sets = []
    for _ in range(3):
        set_emojis = random.sample(ALL_EMOJIS, 3)
        emoji_sets.append(set_emojis)
    return jsonify({"emoji_sets": emoji_sets, "all_emojis": ALL_EMOJIS})


@app.route("/get-reading", methods=["POST"])
def get_reading():
    emoji_sets = request.json.get("emoji_sets")
    if not emoji_sets:
        return jsonify({"error": "No emoji sets provided"}), 400

    # יצירת טקסט תיאורי מהאימוג'ים
    emoji_description = " ".join([" ".join(set_) for set_ in emoji_sets])

    try:
        completion = openai.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=[
                {
                    "role": "system",
                    "content": """אתה קורא בקלפים מיסטי שמפרש אימוג'ים. 
                    עליך לספק קריאה מיסטית ומעניינת בעברית המבוססת על האימוג'ים שניתנו.
                    הקריאה צריכה להיות באורך של 3-4 משפטים.
                    הקריאה צריכה להיות מסתורית אך אופטימית.
                    אל תציין את האימוג'ים עצמם בקריאה.""",
                },
                {
                    "role": "user",
                    "content": f"הנה האימוג'ים לקריאה: {emoji_description}",
                },
            ],
            temperature=0.7,
            max_tokens=200,
        )
        reading = completion.choices[0].message.content
        return jsonify({"reading": reading})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
