# Gemini Image Generator

A tool to create and edit images using Gemini 2.5 Flash Image Preview via Vertex AI.

## Project Structure

```
.
├── .env
├── .env.example
├── assets
│   └── input.png
├── output
│   └── .gitkeep
├── pyproject.toml
└── src
    └── image_generator
        ├── __init__.py
        ├── generator.py
        ├── create_cli.py
        ├── edit_cli.py
        └── main.py
```

*   `assets/`: Holds input images for editing.
*   `output/`: Stores generated and edited images.
*   `src/image_generator/`: The main Python package for the application.
    *   `generator.py`: Contains the core class for interacting with the Gemini API.
    *   `main.py`: Contains the core logic for parsing arguments and dispatching commands.
    *   `create_cli.py`: Entry point for the `create` command.
    *   `edit_cli.py`: Entry point for the `edit` command.

## Installation

1.  **Clone the repository (if you haven't already):**

    ```bash
    git clone https://github.com/your-repo/gemini-image-generator.git
    cd gemini-image-generator
    ```

2.  **Install dependencies using `uv`:**

    ```bash
    uv pip install -e .
    ```

## Configuration

1.  **Create a `.env` file:** Copy the `.env.example` file to `.env`:

    ```bash
    cp .env.example .env
    ```

2.  **Edit `.env`:** Open the newly created `.env` file and replace `"your-gcp-project-id"` with your actual Google Cloud Project ID.

    ```dotenv
    # Google Cloud Project ID
    GOOGLE_CLOUD_PROJECT="your-gcp-project-id"

    # Google Cloud Location (use 'global' for this model)
    GOOGLE_CLOUD_LOCATION="global"

    # Set to True to use Vertex AI backend
    GOOGLE_GENAI_USE_VERTEXAI="True"
    ```

    Alternatively, you can set the `GEMINI_API_KEY` environment variable directly.

    Ensure your Google Cloud environment is authenticated (e.g., via `gcloud auth application-default login`) and Vertex AI is enabled for your project.

## Usage

Commands are run using `uv run <command>`.

### Create an Image

To generate an image from a text prompt:

```bash
uv run create "A futuristic cityscape at sunset, with flying cars and neon lights." -o output/city.png
```

### Edit an Image

To edit an existing image based on a text prompt:

1.  Place the image you want to edit (e.g., `my_input_image.png`) into the `assets/` directory.
2.  Run the edit command, specifying the path to your input image:

    ```bash
    uv run edit "Make this image look like a watercolor painting." assets/my_input_image.png -o output/watercolor_edit.png
    ```

    Replace `my_input_image.png` with the actual filename of your input image.