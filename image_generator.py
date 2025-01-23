import os
import requests
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()


class StabilityImageGenerator:
    def __init__(self):
        self.api_key = os.getenv("STABILITY_API_KEY")
        if not self.api_key:
            raise ValueError("STABILITY_API_KEY environment variable is not set")

        self.base_url = "https://api.stability.ai/v2beta/stable-image/generate/sd3"
        self.headers = {"authorization": f"Bearer {self.api_key}", "accept": "image/*"}

    def generate_images(self, prompts, output_dir="generated_images"):
        """
        Generate images from a list of prompts

        Args:
            prompts (list): List of prompt strings
            output_dir (str): Directory to save generated images
        """
        # Create output directory if it doesn't exist
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # D&D style prefix for all prompts
        dnd_prefix = "Digital art in the style of Dungeons & Dragons fantasy illustration, highly detailed, vibrant colors, dramatic lighting, "

        for i, prompt in enumerate(prompts):
            # Combine the D&D prefix with the original prompt
            enhanced_prompt = dnd_prefix + prompt

            try:
                response = requests.post(
                    self.base_url,
                    headers=self.headers,
                    files={"none": ""},
                    data={
                        "prompt": enhanced_prompt,
                        "output_format": "jpeg",
                    },
                )
                response.raise_for_status()

                if response.status_code == 200:
                    # Extract a descriptive name from the prompt
                    # Take the first part before the colon and convert to snake_case
                    descriptive_name = prompt.split(":")[0].strip().lower().replace(
                        " ", "_"
                    ) or "image_" + datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"{descriptive_name}.jpeg"
                    file_path = output_path / filename

                    # Save the image
                    with open(file_path, "wb") as file:
                        file.write(response.content)

                    print(
                        f"Successfully generated and saved image for prompt {i + 1}: {prompt}"
                    )
                    print(f"Saved to: {file_path}")
                else:
                    print(
                        f"Error generating image for prompt {i + 1}: {response.json()}"
                    )

            except requests.exceptions.RequestException as e:
                print(f"Error generating image for prompt {i + 1}: {str(e)}")


def main():
    # Example prompts - combining modern elements with D&D fantasy style
    prompts = [
        "The Influencer: A charismatic half-elven bard wearing modern streetwear with magical runes, holding both a crystal-powered smartphone and a magical lute. The background shows a modern cityscape transformed by elven architecture, where neon signs mix with magical glowing sigils.",
        "The Coder: A modern wizard in a hoodie decorated with arcane symbols, commanding both a floating magical terminal and ancient scrolls. The room is a tech startup office transformed into a magical sanctum, with monitors displaying both code and magical runes.",
        "The Entrepreneur: A tiefling business-mage in a tailored suit enchanted with golden threads, holding both a magical staff and a modern briefcase leaking ethereal coins. Standing in a magical trading floor where fantasy merchants mix with modern traders.",
        "The Environmentalist: A modern druid in eco-conscious attire merged with living vines, holding a magical tablet displaying world-trees and using magic to purify modern industrial waste into natural energy. Surrounded by both endangered species and magical creatures.",
        "The Gamer: A young battle mage in gaming headset crackling with arcane energy, wielding both modern gaming controllers and magical wands. In a room where arcade machines pulse with real magic and game characters manifest as spectral beings.",
        "The Healer: A modern doctor wearing scrubs emblazoned with healing runes, combining high-tech medical equipment with magical healing arts. The hospital room features both modern medical displays and floating healing crystals.",
        "The Tech Guru: A gnomish innovator in smart glasses that reveal magical auras, surrounded by both floating smartphones and magical constructs. The workspace combines Silicon Valley aesthetic with steampunk-fantasy machinery.",
        "The Minimalist: A contemplative monk in modern minimalist clothing with subtle magical sigils, sitting in a modern apartment transformed into a zen-like magical sanctuary. Clean modern furniture floats alongside ancient magical artifacts, all arranged in perfect geometric harmony.",
        "The Traveler: A person wearing a backpack and holding a map or passport, standing at the edge of a scenic landscape blending mountains, seas, and famous landmarks.",
        "The Activist: A passionate individual holding a protest sign, with a crowd of silhouettes behind them. Vibrant flames or banners ripple in the background.",
        "The Minimalist: A contemplative monk sitting in an ancient temple chamber with clean geometric patterns and magical light. Objects like a levitating plant, an arcane tome, and a floating teacup emphasize magical simplicity.",
        "The Hacker: A mysterious figure in a dark room with glowing green text and cyber symbols around them. Wires and shattered screens form a chaotic yet calculated aesthetic.",
        "The Artist: A creative individual with a paintbrush or digital stylus, surrounded by bursts of color, abstract shapes, and half-formed works of art.",
        "The Athlete: A determined person in sports gear, mid-motion, surrounded by streaks of energy and glowing symbols of strength and vitality.",
        "The Spiritualist: A meditative figure surrounded by modern symbols of spirituality—crystals, glowing orbs, and celestial constellations—set against a cosmic background.",
        "The Musician: A performer with a guitar or microphone, standing under colorful stage lights with musical notes and waves of sound flowing around them.",
        "The Student: A person studying with books, laptops, and glowing knowledge symbols hovering above their head. The backdrop is a modern library or academic setting.",
        "The Chef: A culinary artist holding a pan or knife, surrounded by swirling spices, glowing flames, and plated dishes. A kitchen setting with vibrant lighting completes the scene.",
        "The Visionary: A futuristic figure gazing through high-tech glasses, surrounded by abstract shapes and futuristic cityscapes.",
        "The Parent: A nurturing figure holding a child's hand, with a glowing heart symbol and family-oriented elements like toys, books, and a peaceful home background.",
        "The Wanderer: A lone figure walking along a neon-lit path that fades into the unknown, surrounded by surreal landscapes and glowing symbols of exploration.",
        "The Scientist: A brilliant researcher in a lab coat adorned with glowing equations, surrounded by floating holographic data and experimental apparatus. The lab seamlessly blends cutting-edge technology with mystical energy fields.",
        "The Builder: A master craftsperson wearing augmented reality goggles and traditional work gear, manipulating both physical tools and ethereal construction elements. The background shows impossible architectural wonders under construction.",
        "The Teacher: An inspiring educator standing before a floating array of educational holograms and ancient scrolls, wearing modern professional attire with subtle magical embellishments. The classroom blends high-tech learning tools with magical teaching aids.",
        "The Guardian: A protective figure in modern tactical gear infused with protective runes, wielding both high-tech security devices and magical wards. Standing watch over a modern city protected by both physical and magical security measures.",
        "The Diplomat: A elegant negotiator in formal attire with subtle magical accessories, surrounded by floating translation devices and magical communication orbs. The setting is a modern conference room with elements from multiple magical realms.",
        "The Innovator: A visionary creator in smart clothing with glowing circuit patterns, working with both advanced AI interfaces and ancient invention techniques. Their workshop combines advanced robotics with magical automation.",
        "The Explorer: An adventurous soul in high-tech expedition gear with magical navigation tools, standing at the threshold between known and unknown realms. Equipment combines modern survival gear with magical protection devices.",
        "The Artisan: A skilled creator wearing smart glasses that reveal magical properties of materials, working with both digital design tools and enchanted crafting implements. Their workshop shows both 3D printers and magical forges.",
        "The Mentor: A wise guide in modern clothing with traditional symbolic accessories, surrounded by both digital knowledge repositories and ancient wisdom artifacts. The environment suggests both modern learning and timeless teaching.",
        "The Philosopher: A contemplative figure in a modern study filled with holographic books and floating philosophical diagrams, wearing robes that shift between classical and futuristic styles. Ancient philosophical texts and quantum physics equations intertwine in the air around them.",
        "The Detective: A sharp-minded investigator in a neo-noir trench coat embedded with truth-revealing runes, using both high-tech scanning devices and magical detection spells. The scene shows a crime scene where physical and magical evidence interweaves.",
        "The Chef-Alchemist: A culinary innovator in a kitchen-laboratory hybrid, wearing a chef's coat with alchemical symbols, combining molecular gastronomy equipment with magical brewing apparatus. Floating ingredients and ethereal flavors visible in the air.",
        "The Urban Shaman: A modern spiritual healer in street clothes adorned with tribal patterns that glow with inner light, surrounded by both city spirits and nature spirits. The urban environment shows the hidden magical life of the city.",
        "The Digital Bard: A storyteller surrounded by floating social media feeds and magical storytelling illusions, wearing clothes that shift between pixels and fabric. Their stage is both a streaming setup and a magical performance space.",
        "The Peace Keeper: A diplomatic warrior in adaptive armor that blends military tech with peaceful intentions, carrying both non-lethal weapons and harmony-inducing magical artifacts. The background shows conflict resolution through both technological and magical means.",
        "The Data Mystic: A data scientist wearing augmented reality robes that display real-time information flows, working with both AI systems and divination tools. Their workspace shows the intersection of big data and ancient prophecy.",
        "The Dream Engineer: A sleep specialist in iridescent medical scrubs, working with both advanced sleep monitoring equipment and dream-walking artifacts. The setting is a modern sleep lab where real and dream worlds overlap.",
        "The Quantum Dancer: A performer in a suit that shifts between solid matter and pure energy, manipulating both physical space and probability fields. Their stage exists in multiple dimensions simultaneously.",
        "The Solar Punk: An environmental engineer in biomechanical clothing that photosynthesizes sunlight, combining sustainable technology with earth magic. The background shows a thriving eco-city where nature and technology exist in perfect harmony.",
    ]

    generator = StabilityImageGenerator()
    generator.generate_images(prompts)


if __name__ == "__main__":
    main()
