import asyncio
import nest_asyncio
import uuid
import base64

from openai import AsyncOpenAI
from pathlib import Path

client = AsyncOpenAI()

# Allow nested event loops
nest_asyncio.apply()


async def generate_image(prompt: str, size: str = "1024x1024", quality: str = "medium"):
    response = await client.images.generate(
        model="gpt-image-1", prompt=prompt, size=size, quality=quality
    )

    # Save image
    image_data = base64.b64decode(response.data[0].b64_json)
    filepath = Path("output") / f"{uuid.uuid4()}.png"
    filepath.parent.mkdir(exist_ok=True)
    filepath.write_bytes(image_data)

    return str(filepath)


async def generate_multiple_images(prompts: list[str]):
    tasks = [generate_image(prompt) for prompt in prompts]
    return await asyncio.gather(*tasks)


if __name__ == "__main__":
    prompts = ["anime cat", "anime dog", "anime bird", "anime fish"]
    filepaths = asyncio.run(generate_multiple_images(prompts))
