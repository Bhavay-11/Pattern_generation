import os
import json
from google.cloud import aiplatform
from vertexai.preview.vision_models import ImageGenerationModel
import sys
from PIL import Image

# Define project information


# Initialize Vertex AI
aiplatform.init(project=PROJECT_ID, location=LOCATION)

# Initialize the image generation model
generation_model = ImageGenerationModel.from_pretrained("imagegeneration@006")

# Define input and output folders
input_folder = r"C:\AI dev\img_palette\sona 1708"  # Folder containing JSON files with prompts
output_folder = r"C:\AI dev\img_palette\sona_1708_img"  # Folder to save generated images

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# Function to read prompts from JSON files
def read_prompts_from_folder(folder):
    prompts = []
    for filename in os.listdir(folder):
        if filename.endswith(".json"):
            with open(os.path.join(folder, filename), 'r') as file:
                data = json.load(file)
                prompt = data.get(

                    """Provide a detailed description of the scene in the image, Describe the pattern . We are working on a project that involves creating high-quality, cohesive digital non seamless pattern with distinctive borders.Describe the design of the image be as descriptive as possible.The overall design should be open, with more background color and less busy elements, ensuring a visually appealing and cohesive composition that highlights the cooler tones.The background color should be the most prominent, creating a more open and less busy design Our goal is to produce designs that incorporate a cool tone filter, emphasizing cooler tones . The patterns need to be non seamless with distinctive borders and should use the exact colors present in the image, maintaining the dominance of these colors in descending order . We want to ensure that the final output is vibrant and visually appealing and the design should be 100% similar as the given image.Give text prompt in a single paragraph including the dominant color names in descending order of their percentage value, including the background color name and sub-dominant color name."""

                )
                if prompt:
                    prompts.append((filename, prompt))
    return prompts

# Function to generate and save images
def generate_and_save_images(prompts, model, output_folder, num_images=10):
    for filename, prompt in prompts:
        for i in range(num_images):
            try:
                print(f"Generating image {i+1} for prompt in file: {filename}")
                response = model.generate_images(prompt=prompt)
                if response and response.images:
                    image_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}_{i+1}.png")
                    response.images[0].save(image_path)
                    print(f"Image {i+1} generated and saved as {image_path}")
                else:
                    print(f"No images generated for prompt: {prompt}")
            except Exception as e:
                print(f"Failed to generate image for prompt: {prompt}")
                print(f"Error: {e}")

# Read prompts from the input folder
prompts = read_prompts_from_folder(input_folder)
if not prompts:
    print(f"No prompt files found in the folder: {input_folder}")
    sys.exit(1)

# Generate images and save them to the output folder
generate_and_save_images(prompts, generation_model, output_folder, num_images=10)
