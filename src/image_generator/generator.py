# src/image_generator/generator.py

import os
from io import BytesIO
from pathlib import Path
from typing import Union
import mimetypes

from google import genai
from google.genai.types import GenerateContentConfig, Modality, Part, Blob, Content
from PIL import Image


class GeminiImageGenerator:
    """A class to generate and edit images using the Gemini API via Vertex AI."""

    def __init__(self) -> None:
        """
        Initializes the Gemini client.
        Expects GOOGLE_* environment variables to be set for authentication.
        """
        self.model_name = "gemini-2.5-flash-image-preview"
        try:
            project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
            location = os.getenv("GOOGLE_CLOUD_LOCATION", "global")
            print(f"Using model: {self.model_name}")
            print(f"Using project: {project_id}")
            print(f"Using location: {location}")

            if not project_id:
                raise ValueError(
                    "GOOGLE_CLOUD_PROJECT must be set"
                )

            # Unset API keys to force Vertex AI usage
            os.environ.pop("GOOGLE_API_KEY", None)
            os.environ.pop("GEMINI_API_KEY", None)
            
            self.client = genai.Client(
                project=project_id, location=location, vertexai=True
            )
        except Exception as e:
            print(f"Error initializing Gemini client: {e}")
            print(
                "Please ensure your environment is authenticated with GEMINI_API_KEY or GOOGLE_CLOUD_PROJECT (for Vertex AI)."
            )
            raise

    def _save_image_from_response(
        self, response: genai.types.GenerateContentResponse, output_path: Path
    ) -> None:
        """Extracts and saves an image from a Gemini API response."""
        if (
            response.candidates
            and response.candidates[0].content
            and response.candidates[0].content.parts
        ):
            for part in response.candidates[0].content.parts:
                if part.inline_data and part.inline_data.data:
                    image = Image.open(BytesIO(part.inline_data.data))
                    output_path.parent.mkdir(parents=True, exist_ok=True)
                    image.save(output_path)
                    print(f"Image successfully saved to: {output_path}")
                    return
        print("Warning: No image data found in the response.")

    def create_image(self, prompt: str, output_path: Union[str, Path]) -> None:
        """
        Generates an image from a text prompt.

        Args:
            prompt: The text prompt to generate the image from.
            output_path: The path to save the generated image.
        """
        print(f"Generating image with prompt: '{prompt}'...")
        try:
            contents = prompt
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=contents,
                config=GenerateContentConfig(
                    response_modalities=[Modality.TEXT, Modality.IMAGE]
                ),
            )
            self._save_image_from_response(response, Path(output_path))
        except Exception as e:
            print(f"An error occurred during image creation: {e}")

    def edit_image(
        self,
        prompt: str,
        base_image_path: Union[str, Path],
        output_path: Union[str, Path],
    ) -> None:
        """
        Edits an existing image based on a text prompt.

        Args:
            prompt: The text prompt describing the edit.
            base_image_path: The path to the image to be edited.
            output_path: The path to save the edited image.
        """
        print(f"Editing image '{base_image_path}' with prompt: '{prompt}'...")
        try:
            mime_type, _ = mimetypes.guess_type(base_image_path)
            if not mime_type or not mime_type.startswith("image"):
                raise ValueError(f"Could not determine image type for {base_image_path}")

            with open(base_image_path, "rb") as f:
                image_bytes = f.read()

            blob = Blob(data=image_bytes, mime_type=mime_type)
            image_part = Part(inline_data=blob)
            text_part = Part(text=prompt)

            contents = Content(role="user", parts=[text_part, image_part])

            response = self.client.models.generate_content(
                model=self.model_name,
                contents=contents,
                config=GenerateContentConfig(
                    response_modalities=[Modality.TEXT, Modality.IMAGE]
                ),
            )
            self._save_image_from_response(response, Path(output_path))
        except FileNotFoundError:
            print(f"Error: Base image not found at '{base_image_path}'")
        except Exception as e:
            print(f"An error occurred during image editing: {e}")