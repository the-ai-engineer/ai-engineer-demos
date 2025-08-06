"""
Parallel Image Generation using OpenAI's gpt-image-1 model.

See: https://platform.openai.com/docs/api-reference/images

Usage:
    # Set environment variable
    export OPENAI_API_KEY="your-api-key"

    # Basic usage
    generator = ImageGenerator()
    prompts = ["A cat", "A dog", "A bird"]
    filepaths = await generator.generate_images(prompts)

    # Custom configuration
    generator = ImageGenerator(
        output_dir="my_images",
        image_size="1024x1024",
        image_quality="medium"
    )
"""

import aiohttp
import asyncio
import base64
import os
import time
import aiofiles

from pathlib import Path
from typing import List, Optional


# Constants
DEFAULT_IMAGE_SIZE = "1024x1536"
DEFAULT_IMAGE_QUALITY = "high"


class ImageGenerator:
    def __init__(
        self,
        api_key: Optional[str] = None,
        output_dir: str = "output/images",
        image_size: str = DEFAULT_IMAGE_SIZE,
        image_quality: str = DEFAULT_IMAGE_QUALITY,
    ) -> None:
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.output_dir = Path(output_dir)
        self.image_size = image_size
        self.image_quality = image_quality
        self.output_dir.mkdir(parents=True, exist_ok=True)

        if not self.api_key:
            raise ValueError(
                "OPENAI_API_KEY environment variable or api_key parameter required"
            )

    async def generate_image(
        self, session: aiohttp.ClientSession, prompt: str
    ) -> Optional[str]:
        """Generate a single image from prompt"""
        payload = {
            "model": "gpt-image-1",
            "prompt": prompt,
            "size": self.image_size,
            "quality": self.image_quality,
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        try:
            async with session.post(
                "https://api.openai.com/v1/images/generations",
                json=payload,
                headers=headers,
            ) as response:
                if response.status != 200:
                    error = await response.text()
                    raise Exception(f"API error {response.status}: {error}")

                data = await response.json()
                if not data.get("data") or len(data["data"]) == 0:
                    raise Exception("No image data returned from API")
                image_data = data["data"][0]["b64_json"]

                return await self._save_base64_image(image_data)

        except Exception as e:
            print(f"Failed to generate image: {e}")
            return None

    async def _save_base64_image(self, base64_data: str) -> str:
        """Save base64 image data to output directory"""

        timestamp = str(time.time_ns())
        filepath = self.output_dir / f"{timestamp}.png"

        try:
            image_bytes = base64.b64decode(base64_data)
            async with aiofiles.open(filepath, "wb") as f:
                await f.write(image_bytes)
            return str(filepath)
        except Exception as e:
            print(f"Failed to save image: {e}")
            return None

    async def generate_images(self, prompts: List[str]) -> List[str]:
        """Generate multiple images from formatted prompts

        Args:
            prompts: List of formatted prompt strings
        """
        if not prompts:
            return []

        async with aiohttp.ClientSession() as session:
            tasks = [self.generate_image(session, prompt) for prompt in prompts]

            results = await asyncio.gather(*tasks, return_exceptions=True)

            # Filter successful results and handle errors
            successful = []
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    print(f"Failed to generate image for prompt {i + 1}: {result}")
                elif result:
                    successful.append(result)

            print(f"Generated {len(successful)}/{len(prompts)} images successfully")
            for filepath in successful:
                print(f"  → {filepath}")

            return successful


if __name__ == "__main__":
    # Example usage
    async def main() -> None:
        generator = ImageGenerator()
        prompts = [
            "A cute kitten playing with a ball of yarn",
            "A tiny frog sitting on a lily pad",
            "A whimsical treehouse in a magical forest",
        ]
        await generator.generate_images(prompts)

    asyncio.run(main())
