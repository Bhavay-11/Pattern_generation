import os
from PIL import Image, ImageEnhance

def make_image_warmer(input_folder, output_folder, enhancement_factor=1.2):
    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Iterate through all files in the input folder
    for filename in os.listdir(input_folder):
        # Construct the full file path
        input_image_path = os.path.join(input_folder, filename)
        
        # Check if the file is an image (you can add more extensions if needed)
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            # Open the image
            with Image.open(input_image_path) as img:
                # Check if the image has an alpha channel
                if img.mode == 'RGBA':
                    r, g, b, a = img.split()
                else:
                    r, g, b = img.split()
                    a = None  # No alpha channel
                
                # Enhance the red and green channels to increase warmth
                r = ImageEnhance.Brightness(r).enhance(enhancement_factor*0.7)
                g = ImageEnhance.Brightness(g).enhance(enhancement_factor*0.7)  # Slightly less for green

                if a:
                    # Merge the channels back including alpha
                    warmer_img = Image.merge("RGBA", (r, g, b, a))
                else:
                    # Merge the channels back without alpha
                    warmer_img = Image.merge("RGB", (r, g, b))

                # Construct the output file path
                output_image_path = os.path.join(output_folder, filename)
                
                # Save the new image
                warmer_img.save(output_image_path)
                
                print(f"Processed and saved: {output_image_path}")

# Example usage
input_folder = r'C:\AI dev\img_palette\versace_warm'
output_folder = r'C:\AI dev\img_palette\versace_warm_op'
make_image_warmer(input_folder, output_folder)
