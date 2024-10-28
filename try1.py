import cv2
import numpy as np
import matplotlib.pyplot as plt
import json
import os
import time
from sklearn.cluster import KMeans

# Function to generate a color description with retries
# def retry_api_call(func, *args, **kwargs):
#     retries = 5
#     delay = 10  # Initial delay in seconds
#     for i in range(retries):
#         try:
#             return func(*args, **kwargs)
#         except openai.error.RateLimitError as e:
#             print(f"Rate limit error: {e}. Retrying in {delay} seconds...")
#             time.sleep(delay)
#             delay *= 2  # Exponential backoff
#     raise Exception("API rate limit exceeded. Please try again later.")

# def describe_color(hex_code):
#     prompt = f"Describe the color {hex_code}. Include its characteristics and how it feels."
#     response = retry_api_call(
#         openai.ChatCompletion.create,
#         model="gpt-3.5-turbo",
#         messages=[
#             {"role": "system", "content": "You are an expert in describing colors."},
#             {"role": "user", "content": prompt}
#         ]
#     )
#     return response.choices[0].message['content'].strip()

def rgb_to_hex(color):
    """Converts an RGB color to HEX format."""
    return "#{:02x}{:02x}{:02x}".format(int(color[0]), int(color[1]), int(color[2]))

def closest_color(requested_color):
    """Find the closest color name for a given RGB color."""
    min_colors = {}
    for key, name in webcolors.CSS3_HEX_TO_NAMES.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_color[0]) ** 2
        gd = (g_c - requested_color[1]) ** 2
        bd = (g_c - requested_color[2]) ** 2
        min_colors[(rd + gd + bd)] = name
    return min_colors[min(min_colors.keys())]

def get_colors(image, min_percentage=0.01):
    """Gets the most common colors in an image dynamically."""
    # Reshape the image to be a list of pixels
    pixels = np.float32(image.reshape(-1, 3))
    
    # Initial number of clusters
    num_clusters = 10
    clusters = KMeans(n_clusters=num_clusters)
    labels = clusters.fit_predict(pixels)
    palette = clusters.cluster_centers_
    
    # Count each label frequency
    counts = np.bincount(labels)
    
    # Calculate percentage of each color
    percentages = counts / counts.sum()
    
    # Filter colors by minimum percentage
    filtered_indices = np.where(percentages >= min_percentage)[0]
    while len(filtered_indices) < num_clusters:
        num_clusters -= 1
        clusters = KMeans(n_clusters=num_clusters)
        labels = clusters.fit_predict(pixels)
        palette = clusters.cluster_centers_
        counts = np.bincount(labels)
        percentages = counts / counts.sum()
        filtered_indices = np.where(percentages >= min_percentage)[0]
    
    dominant_colors = palette[filtered_indices]
    percentages = percentages[filtered_indices]
    
    return dominant_colors, percentages

def plot_colors(colors):
    """Plots the colors without hex codes and percentages."""
    fig, ax = plt.subplots(1, 1, figsize=(12, 2),
                           subplot_kw=dict(xticks=[], yticks=[], frame_on=False))
    col_width = 1 / len(colors)
    for i, color in enumerate(colors):
        ax.add_patch(plt.Rectangle((i * col_width, 0), col_width, 1,
                                   color=np.array(color)/255.0))
    plt.show()

def process_image(image_path, min_percentage=0.01):
    """Process a single image to detect colors and generate palette image."""
    # Check if the image path exists
    if not os.path.isfile(image_path):
        print(f"Error: The file {image_path} does not exist.")
        return

    # Read the image
    image = cv2.imread(image_path)
    
    # Check if the image was loaded successfully
    if image is None or image.size == 0:
        print(f"Error: Unable to read the image file {image_path}.")
        return
    
    # Convert image to RGB
    try:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    except cv2.error as e:
        print(f"Error: {e}")
        return
    
    # Get colors and their percentages
    colors, _ = get_colors(image, min_percentage)
    
    # Plot the colors
    plot_colors(colors)
    
    # Save the palette image
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    output_file = f'{output_folder}/{base_name}_palette.png'
    plt.savefig(output_file, bbox_inches='tight', pad_inches=0)
    plt.close()
    print(f'Palette image saved to {output_file}')

def process_folder(input_folder, output_folder, min_percentage=0.01):
    """Process all images in the input folder and save palette images to output folder."""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for filename in os.listdir(input_folder):
        if filename.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
            image_path = os.path.join(input_folder, filename)
            process_image(image_path, min_percentage)

# Example usage
input_folder = 'C:\AI dev\img_palette\input_folder'  # Replace with your input folder path
output_folder = 'C:\AI dev\img_palette\output_folder'  # Replace with your output folder path
process_folder(input_folder, output_folder, min_percentage=0.01)
