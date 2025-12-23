import os
import json
from PIL import Image
from PIL.ExifTags import TAGS


class CustomJSONEncoder(json.JSONEncoder):
    """ Custom JSON Encoder to handle non-serializable types like IFDRational from PIL. """
    def default(self, obj):
        if isinstance(obj, Image.Exif):
            return {TAGS.get(k, k): self.default(v) for k, v in obj.items()}
        elif hasattr(obj, 'numerator') and hasattr(obj, 'denominator'):
            # Convert IFDRational to a simple fraction string
            return f"{obj.numerator}/{obj.denominator}"
        return super().default(obj)

def get_selected_exif_data(image_path, selected_tags):
    """Extract selected EXIF data from an image."""
    try:
        image = Image.open(image_path)
        exif_data = {}

        if image._getexif() is not None:
            for tag, value in image._getexif().items():
                decoded_tag = TAGS.get(tag, tag)
                if decoded_tag in selected_tags:
                    exif_data[decoded_tag] = value

        return exif_data
    except IOError:
        return None

def read_selected_exif_data_from_folder(folder_path, selected_tags):
    """Read selected EXIF data from images in a specified folder."""
    exif_data = {}
    
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
            file_path = os.path.join(folder_path, filename)
            exif_data[filename] = get_selected_exif_data(file_path, selected_tags)

    return exif_data

# Specified attributes
selected_attributes = ['Make', 'Model', 'ISOSpeedRatings', 'ExposureMode', 'FocalLength', 'FNumber']

# Example usage
folder_path = 'media/gallery'
exif_data = read_selected_exif_data_from_folder(folder_path, selected_attributes)

# Saving the data to a JSON file using the custom encoder
with open('selected_exif_data.json', 'w') as file:
    json.dump(exif_data, file, cls=CustomJSONEncoder, indent=4)



