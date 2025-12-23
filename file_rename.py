import os

def rename_images(folder_path):
    # List all files in the folder
    files = os.listdir(folder_path)

    # Filter out files that are images
    image_files = [file for file in files if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]

    # Sort files alphabetically to maintain a specific order
    image_files.sort()

    # Rename each image file
    for i, file in enumerate(image_files):
        # Construct new file name
        new_name = f"{i+1}.jpg"

        # Construct full file paths
        old_file = os.path.join(folder_path, file)
        new_file = os.path.join(folder_path, new_name)

        # Rename the file
        os.rename(old_file, new_file)

    return f"Renamed {len(image_files)} images in the folder '{folder_path}'."

# Example usage
folder_path = "media/gallery"
rename_images_result = rename_images(folder_path)
rename_images_result
