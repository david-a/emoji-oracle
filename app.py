import os
import random
from dotenv import load_dotenv
from openai import OpenAI
from flask import Flask, render_template, jsonify, redirect, url_for

# טעינת משתני הסביבה
load_dotenv()

app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_random_images():
    """בחירת 3 תמונות אקראיות מהתיקייה"""
    images_dir = "generated_images"
    all_images = [f for f in os.listdir(images_dir) if f.endswith(".jpeg")]
    selected = random.sample(all_images, 3)
    return [
        {
            "path": f"/static/generated_images/{img}",
            "name": img.replace(".jpeg", "").replace("the_", ""),
        }
        for img in selected
    ]


def get_prediction(archetypes):
    """קבלת חיזוי מ-OpenAI"""
    prompt = f"""בהתבסס על שלושת הארכיטיפים הבאים: {', '.join(archetypes)},
    צור תחזית עתיד חיובית ומעוררת השראה בעברית(3-4 משפטים).
    התחזית צריכה להיות אישית, מעודדת ואופטימית ונכתבת בגוף שני.
    חשוב שהתחזית תהיה מפורטת ותתייחס לכל אחד מהארכיטיפים."""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=500,
        )
        return response.choices[0].message.content
    except Exception as e:
        return str(e)


@app.route("/")
def index():
    """דף הבית"""
    images = get_random_images()
    return render_template("index.html", images=images)


@app.route("/new-game")
def new_game():
    """התחלת משחק חדש"""
    return redirect(url_for("index"))


@app.route("/predict/<path:archetypes>")
def predict(archetypes):
    """נקודת קצה לקבלת חיזוי"""
    archetype_list = archetypes.split(",")
    prediction = get_prediction(archetype_list)
    return jsonify({"prediction": prediction})


if __name__ == "__main__":
    # העתקת התמונות לתיקיית static
    os.makedirs("static/generated_images", exist_ok=True)
    for img in os.listdir("generated_images"):
        if img.endswith(".jpeg"):
            src = os.path.join("generated_images", img)
            dst = os.path.join("static/generated_images", img)
            if not os.path.exists(dst):
                os.system(f'cp "{src}" "{dst}"')

    app.run(debug=True)
