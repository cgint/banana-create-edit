# src/image_generator/main.py

import argparse
import sys
from dotenv import load_dotenv
from image_generator.generator import GeminiImageGenerator
from pathlib import Path


def _run_cli_logic() -> None:
    """Internal function to run the image generator from the command line."""
    load_dotenv(override=True)

    parser = argparse.ArgumentParser(
        description="Create and edit images with Gemini 2.5 Flash Image Preview."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Create command
    create_parser = subparsers.add_parser("create", help="Create an image from a prompt.")
    create_parser.add_argument("prompt", type=str, help="The text prompt.")
    create_parser.add_argument(
        "-o",
        "--output",
        type=str,
        default="output/generated_image.png",
        help="Output path for the generated image.",
    )

    # Edit command
    edit_parser = subparsers.add_parser("edit", help="Edit an existing image.")
    edit_parser.add_argument("prompt", type=str, help="The text prompt for editing.")
    edit_parser.add_argument(
        "image_path", type=str, help="Path to the base image to edit."
    )
    edit_parser.add_argument(
        "-o",
        "--output",
        type=str,
        default="output/edited_image.png",
        help="Output path for the edited image.",
    )

    args = parser.parse_args()

    try:
        generator = GeminiImageGenerator()
        if args.command == "create":
            generator.create_image(prompt=args.prompt, output_path=args.output)
            # Persist the prompt with the same base name as the output image
            output_path_obj = Path(args.output)
            prompt_file_path = output_path_obj.with_suffix(".prompt.txt")
            prompt_file_path.parent.mkdir(parents=True, exist_ok=True)
            prompt_file_path.write_text(args.prompt)
            print(f"Prompt saved to: {prompt_file_path}")
        elif args.command == "edit":
            generator.edit_image(
                prompt=args.prompt,
                base_image_path=args.image_path,
                output_path=args.output,
            )
            # Persist the prompt with the same base name as the output image
            output_path_obj = Path(args.output)
            prompt_file_path = output_path_obj.with_suffix(".prompt.txt")
            prompt_file_path.parent.mkdir(parents=True, exist_ok=True)
            prompt_file_path.write_text(args.prompt)
            print(f"Prompt saved to: {prompt_file_path}")
    except Exception:
        print("Failed to execute the command. Please check your configuration and arguments.")


def main_create() -> None:
    """Entry point for the 'create' command."""
    sys.argv.insert(1, "create")
    _run_cli_logic()


def main_edit() -> None:
    """Entry point for the 'edit' command."""
    sys.argv.insert(1, "edit")
    _run_cli_logic()