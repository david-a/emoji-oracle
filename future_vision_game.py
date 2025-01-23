import os
import random
from dotenv import load_dotenv
from openai import OpenAI

# טעינת משתני הסביבה
load_dotenv()


class FutureVisionGame:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.selected_images = self.choose_random_images()
        self.play_game()

    def choose_random_images(self):
        """בחירת 3 תמונות אקראיות מהתיקייה"""
        images_dir = "generated_images"
        all_images = [f for f in os.listdir(images_dir) if f.endswith(".jpeg")]
        selected = random.sample(all_images, 3)
        return selected

    def play_game(self):
        """הפעלת המשחק"""
        # הצגת התמונות שנבחרו
        archetypes = [
            img.replace(".jpeg", "").replace("the_", "") for img in self.selected_images
        ]

        print("\n" + "=" * 50)
        print("ברוכים הבאים למשחק חזון העתיד!")
        print("=" * 50 + "\n")
        print("הארכיטיפים שנבחרו עבורך הם:")
        for archetype in archetypes:
            print(f"- {archetype}")
        print("\n" + "=" * 50 + "\n")

        # יצירת החיזוי
        self.get_prediction(archetypes)

    def get_prediction(self, archetypes):
        """קבלת חיזוי מ-OpenAI"""
        prompt = f"""בהתבסס על שלושת הארכיטיפים הבאים: {', '.join(archetypes)},
        צור תחזית עתיד חיובית ומעוררת השראה בעברית (כ-3 משפטים).
        התחזית צריכה להיות אישית, מעודדת ואופטימית."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=200,
            )

            prediction = response.choices[0].message.content
            print("חזון העתיד שלך:")
            print("-" * 20)
            print(prediction)
            print("-" * 20 + "\n")

        except Exception as e:
            print(f"\nשגיאה: {str(e)}\n")


if __name__ == "__main__":
    game = FutureVisionGame()
