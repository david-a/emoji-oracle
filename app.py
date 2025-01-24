from flask import Flask, render_template, jsonify, request
import random
import json
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# Load emoji data
def load_emojis():
    current_dir = Path(__file__).parent
    with open(current_dir / "data" / "emojis.json", "r", encoding="utf-8") as f:
        return json.load(f)


class EmojiReader:
    def __init__(self):
        self.emojis = load_emojis()["emojis"]

    def generate_emoji_sets(self):
        """Generate 3 sets of 3 random emojis"""
        sets = []
        for _ in range(3):
            emoji_set = random.sample(self.emojis, 3)
            sets.append(emoji_set)
        return sets

    def get_reading(self, emoji_sets):
        """Get a mystical reading based on the emoji combinations"""
        emoji_description = "\n".join(
            [f"סט {i+1}: {' '.join(set)}" for i, set in enumerate(emoji_sets)]
        )

        prompt = f"""אתה ״הקורא באמוג'י״ שקורא את סיפורו של האדם שמולך דרך שילובי אמוג'ים.
        הוצגו בפניך שלושה סטים של אמוג'ים:
        
        {emoji_description}
        
        ספק קריאה יצירתית, מיסטית ומעניינת ש:
        1. מפרשת הסט הראשון כמייצג עבר, השני כמייצג הווה והשלישי כמייצג עתיד
        2. מוצאת קשרים בין הסטים
        3. מציעה תובנות והכוונה עדינה
        4. שומרת על טון מיסטי אך משחקי
        5. חשוב מאוד שהסיפור יתאר מגמה חיובית וטובה
        
        שמור על תשובה קצרה וזורמת של עד 250 מילים ועצב אותה יפה עם קישוטי אמוג'י."""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": prompt}],
            temperature=0.8,
        )

        return response.choices[0].message.content


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/generate-emojis", methods=["GET"])
def generate_emojis():
    reader = EmojiReader()
    emoji_sets = reader.generate_emoji_sets()
    all_emojis = reader.emojis  # שולח את כל האימוג'ים האפשריים
    return jsonify({"emoji_sets": emoji_sets, "all_emojis": all_emojis})


@app.route("/get-reading", methods=["POST"])
def get_reading():
    emoji_sets = request.json["emoji_sets"]
    reader = EmojiReader()
    reading = reader.get_reading(emoji_sets)
    return jsonify({"reading": reading})


if __name__ == "__main__":
    app.run(debug=True)
