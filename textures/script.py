import os
from PIL import Image

# Specify the folder containing the PNG images
folder_path = os.getcwd()

# Specify the target size (width, height)
target_size = (100, 100)  # Example: Resize to 800x600

# Loop through all files in the folder
for filename in os.listdir(folder_path):
    # Check if the file is a PNG
    if filename.lower().endswith('.png'):
        # Create the full path to the image file
        file_path = os.path.join(folder_path, filename)
        
        # Open the image
        with Image.open(file_path) as img:
            # Resize the image
            resized_img = img.resize(target_size)
            
            # Save the resized image back to the same location
            resized_img.save(file_path)
            print(f"Resized {filename} to {target_size}")

print("All PNG images have been resized.")