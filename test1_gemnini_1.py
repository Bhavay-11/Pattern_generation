import google.generativeai as genai
import PIL.Image
import os
import json

# Configure your API key
GOOGLE_API_KEY = "AIzaSyAaWpyblCGoK0y6PJlbn535WhL8-w6gOlU"
genai.configure(api_key=GOOGLE_API_KEY)

# Define input and output folders
input_folder = r'D:\Desktop\0609emb'
output_folder = r'C:\AI dev\img_palette\69_op'

#"Provide a detailed description of the scene in the image including dominant, background color,sub-dominant , style and tone of the image in this same order itself in this same order itself.And with correct hexcodes and color names also include exact percentage of each color present.",
# List of prompts
#Include color names in descending order and include seamless word one time .Only give a text prompt to create an abstract geometric seamless similar pattern based on the dominant color name, background color name, sub-dominant color name, style and tone of the image .Mentioned values should be in this specific order only dominant colors names should be in descending order only based on their percentage value and make sure that it only includes the exact colors present in image (and pattern should be absolutely seamless) everything should be as elaborate as possible. Also apply a cool tone filter on every image be as less creative as possible and only create similar design in terms of creating a design for cooler tones of these colors and also apply cool filter on all patterns
#Give text prompt in a single paragraph including the dominant color names in descending order of their percentage value, including the background color name and sub-dominant color name, with a cool tone filter applied. The design should incorporate dominant colors in descending order, the background color, and the sub-dominant color, emphasizing cooler tones. Ensure the pattern is absolutely seamless and maintains an abstract geometric style, applying a cool tone filter to the entire design for a high-quality, cohesive look
#Give text prompt in a single paragraph including the dominant color names in descending order of their percentage value, including the background color name and sub-dominant color name, with a cool tone filter applied. The design should incorporate dominant colors in descending order, the background color, and the sub-dominant color, emphasizing cooler tones. Ensure the pattern is absolutely seamless and maintains an abstract geometric style, applying a cool tone filter to the entire design for a high-quality, cohesive look only in black and white color 2d abstract design
#abstract floral, network,chevron
#Provide a detailed description of the scene in the image, Describe the pattern , content of image as much as possible. We are working on a project that involves creating high-quality, cohesive digital textile prints with a seamless pattern.Describe the design of the image be as descriptive as possible. Our goal is to produce designs that incorporate a cool tone filter, emphasizing cooler tones and the design should be 100% similar as the given image. The patterns need to be 100% seamless and should use the exact colors present in the image, maintaining the dominance of these colors in descending order . We want to ensure that the final output is vibrant and visually appealing and the design should be 100% similar as the given image.Give text prompt in a single paragraph including the dominant color names in descending order of their percentage value, including the background color name and sub-dominant color name, with a cool tone filter applied and the design should be 100% similar as the given image.
prompts=[
    

    """Provide a detailed description of the scene in the image, Describe the pattern . We are working on a project that involves creating high-quality, cohesive digital seamless pattern.Describe the design of the image be as descriptive as possible.The overall design should be open, with more background color and less busy elements, ensuring a visually appealing and cohesive composition that highlights the cooler tones.The background color should be the most prominent, creating a more open and less busy design Our goal is to produce designs that incorporate a cool tone filter, emphasizing cooler tones . The patterns need to be non seamless with distinctive borders and should use the exact colors present in the image, maintaining the dominance of these colors in descending order . We want to ensure that the final output is vibrant and visually appealing and the design should be 100% similar as the given image.Give text prompt in a single paragraph including the dominant color names in descending order of their percentage value, including the background color name and sub-dominant color name."""
    ]

# prompts = [
   
#     "What is in this photo?",
#     "Describe the dominant colors in this image.",
#     "What style and tone does this image possess?",
#     "Provide a detailed description of the scene in the image including dominant, background color,sub-dominant , style and tone of the image in this same order itself."
# ]
# # Ensure output folder exists
os.makedirs(output_folder, exist_ok=True)

# Process each image in the input folder
for filename in os.listdir(input_folder):
    if filename.endswith('.png') or filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.tiff') or filename.endswith('.tif'):
        img_path = os.path.join(input_folder, filename)
        img = PIL.Image.open(img_path)
        
        # Generate responses for each prompt
        responses = {}
        for prompt in prompts:
            response = genai.GenerativeModel(model_name="gemini-1.5-flash").generate_content([prompt, img])
            responses[prompt] = response.text

        # Save the responses to a JSON file
        output_file = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}_responses.json")
        with open(output_file, 'w') as f:
            json.dump(responses, f, indent=4)

        print(f"Responses for {filename} saved to {output_file}")