import os
import json
import sys
import requests
from PIL import Image
from openai import AzureOpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_ENDPOINT = "https://shaddyy.openai.azure.com/"

# Initialize Azure OpenAI client
client = AzureOpenAI(
    api_version="2024-02-01",
    azure_endpoint=AZURE_ENDPOINT,
    api_key=AZURE_OPENAI_API_KEY,
)

# Define input and output folders
input_folder = r"C:\AI dev\img_palette\1_opppp"  # Folder containing JSON files with prompts
output_folder = r"C:\AI dev\img_palette\1_imgggg"  # Folder to save generated images

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
                    """Provide a detailed description of the scene in the image, Describe the pattern . We are working on a project that involves creating high-quality, cohesive digital  seamless pattern.Describe the design of the image be as descriptive as possible.The overall design should be open, with more background color and less busy elements, ensuring a visually appealing and cohesive composition that highlights the cooler tones.The background color should be the most prominent, creating a more open and less busy design \n    Our goal is to produce designs that incorporate a cool tone filter, emphasizing cooler tones . \n    The patterns need to be 100% seamless and should use the exact colors present in the image, maintaining the dominance of these colors in descending order . \n    We want to ensure that the final output is vibrant and visually appealing and the design should be 100% similar as the given image.\n    Give text prompt in a single paragraph including the dominant color names in descending order of their percentage value, including the background color name and sub-dominant color name."""
                )
                if prompt:
                    prompts.append((filename, prompt))
    return prompts

# Function to generate and save images using Azure OpenAI
def generate_and_save_images(prompts, client, output_folder, num_images=10):
    for filename, prompt in prompts:
        for i in range(num_images):
            try:
                print(f"Generating image {i+1} for prompt in file: {filename}")
                result = client.images.generate(
                    model="Dalle3",
                    prompt=prompt,
                    n=1
                )
                image_url = json.loads(result.model_dump_json())['data'][0]['url']
                
                # Save image
                image_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}_{i+1}.png")
                with open(image_path, 'wb') as file:
                    file.write(requests.get(image_url).content)
                
                print(f"Image {i+1} generated and saved as {image_path}")
            except Exception as e:
                print(f"Failed to generate image for prompt: {prompt}")
                print(f"Error: {e}")

# Read prompts from the input folder
prompts = read_prompts_from_folder(input_folder)
if not prompts:
    print(f"No prompt files found in the folder: {input_folder}")
    sys.exit(1)

# Generate images and save them to the output folder
generate_and_save_images(prompts, client, output_folder, num_images=10)