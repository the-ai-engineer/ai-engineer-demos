import uuid
import base64

from openai import OpenAI
from pathlib import Path

client = OpenAI()


def generate_image(prompt: str, size: str = "1024x1024", quality: str = "medium"):
    response = client.images.generate(
        model="gpt-image-1", prompt=prompt, size=size, quality=quality
    )

    # Save image
    image_data = base64.b64decode(response.data[0].b64_json)
    filepath = Path("output") / f"{uuid.uuid4()}.png"
    filepath.write_bytes(image_data)

    return str(filepath)


if __name__ == "__main__":
    prompts = ["anime cat", "anime dog", "anime bird", "anime fish"]
    for prompt in prompts:
        filepath = generate_image(prompt)
        print(f"Generated image for '{prompt}': {filepath}")
