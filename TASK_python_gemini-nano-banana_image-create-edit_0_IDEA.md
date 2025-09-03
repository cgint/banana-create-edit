<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# i need working code in python on how to connect to latest nano banana via vertex ai to create and edit images using gemini-2.5-flash-image-preview

Here is working **Python code** to connect to the latest **Nano Banana (Gemini-2.5-Flash-Image-Preview)** model via **Vertex AI** for creating and editing images. This code uses the official `google-genai` SDK and is based on up-to-date documentation and production samples.[^1_1][^1_2][^1_3]

## Installation and Setup

Make sure you have enabled Vertex AI on your Google Cloud project and set up billing and authentication (service account or application default credentials). Install the SDK:

```bash
pip install --upgrade google-genai
```

Set environment variables for Vertex AI:

```bash
export GOOGLE_CLOUD_PROJECT=[YOUR_PROJECT_ID]
export GOOGLE_CLOUD_LOCATION=global
export GOOGLE_GENAI_USE_VERTEXAI=True
```

Replace `[YOUR_PROJECT_ID]` with your actual GCP project ID.

## Python Code: Create and Edit Images

The following code demonstrates both image creation (from prompt) and editing (from prompt + image):

```python
from google import genai
from google.genai.types import GenerateContentConfig, Modality
from PIL import Image
from io import BytesIO

# Create a Gemini client (uses credentials from your environment)
client = genai.Client()

# ------- Image Creation (text-to-image) -------
prompt = "Create a picture of a cat eating a nano banana in a fancy restaurant under the Gemini constellation."

response = client.models.generate_content(
    model="gemini-2.5-flash-image-preview",
    contents=[prompt],
    config=GenerateContentConfig(response_modalities=[Modality.TEXT, Modality.IMAGE])
)

for part in response.candidates.content.parts:
    if part.text:
        print(part.text)
    elif part.inline_data:
        image = Image.open(BytesIO(part.inline_data.data))
        image.save("generated_image.png")

# ------- Image Editing (image + prompt) -------
# Load your existing image
base_image = Image.open("input.png")  # Path to your image file

edit_prompt = "Edit this image to make it look like a cartoon."
response = client.models.generate_content(
    model="gemini-2.5-flash-image-preview",
    contents=[base_image, edit_prompt],
    config=GenerateContentConfig(response_modalities=[Modality.TEXT, Modality.IMAGE])
)

for part in response.candidates.content.parts:
    if part.text:
        print(part.text)
    elif part.inline_data:
        edited_image = Image.open(BytesIO(part.inline_data.data))
        edited_image.save("edited_image.png")
```

- The **text-to-image** section generates a new image from a prompt.
- The **image editing** section applies edits to an existing image as described in the prompt.[^1_2][^1_3][^1_1]
- Both parts use the officially supported `generate_content` method with the `gemini-2.5-flash-image-preview` model.
- Images are returned as binary data and can be saved via Pillow's `Image.save()` after parsing with `BytesIO`.


## Additional Notes

- API authentication is handled via Google credentials in your environment.[^1_4][^1_3]
- Replace paths and prompts as needed for your use case.
- Edits, multi-image blending, local edits, and conversational multi-turn editing are all supported by modifying the input to `contents`.[^1_3][^1_2]

This approach ensures access to **all Gemini-2.5-Flash (Nano Banana)** image generation and editing capabilities directly from Python via Vertex AI with the latest official API.[^1_3]
<span style="display:none">[^1_10][^1_5][^1_6][^1_7][^1_8][^1_9]</span>

<div style="text-align: center">⁂</div>

[^1_1]: https://developers.googleblog.com/en/introducing-gemini-2-5-flash-image/

[^1_2]: https://zenn.dev/saan/articles/0034159803b3aa

[^1_3]: https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/image-editing

[^1_4]: https://apidog.com/blog/nano-banana-via-api/

[^1_5]: https://www.youtube.com/watch?v=rV8NqpkklNU

[^1_6]: https://ai.google.dev/gemini-api/docs/image-generation

[^1_7]: https://cloud.google.com/blog/products/ai-machine-learning/gemini-2-5-flash-image-on-vertex-ai

[^1_8]: https://cloud.google.com/vertex-ai/generative-ai/docs/image/edit-images-overview

[^1_9]: https://clickkatha.com/blog/How-to-use-Google-Nano-Banana-AI-the-complete-2025-guide

[^1_10]: https://cloud.google.com/vertex-ai/generative-ai/docs/models/gemini/2-5-flash

