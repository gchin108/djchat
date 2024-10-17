from PIL import Image
import os
from django.core.exceptions import ValidationError


def validate_icon_image_size(image):
    if image:
        with Image.open(image) as img:
            if img.width > 70 or img.height > 70:
                raise ValidationError("Icon size should be 70x70")


def validate_image_file_extension(image):
    if image:
        extension = os.path.splitext(image.name)[1]
        if extension.lower() not in [".jpg", ".jpeg", ".png", ".gif"]:
            raise ValidationError(
                "File extension not supported. Supported extensions: .jpg, .jpeg, .png and .gif"
            )
