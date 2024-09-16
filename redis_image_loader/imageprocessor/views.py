from django.shortcuts import render

# Create your views here.
import os
from PIL import Image
from django.http import JsonResponse
from django.conf import settings

# Redis instance from settings.py
redis_instance = settings.redis_instance

# Directory where the images will be mounted
IMAGE_DIR = '/images'

def convert_and_store_image(image_path):
    # Open the image file
    with Image.open(image_path) as img:
        # Convert to 6-bit
        img = img.convert('P', palette=Image.ADAPTIVE, colors=64)
        # Save the image to a temporary location in memory
        img.save(f'/tmp/{os.path.basename(image_path)}', 'PNG')

        # Read the file into memory and store it in Redis
        with open(f'/tmp/{os.path.basename(image_path)}', 'rb') as f:
            redis_instance.set(f"image:{os.path.basename(image_path)}", f.read())

def load_images_to_redis(request):
    image_files = os.listdir(IMAGE_DIR)

    for image_file in image_files:
        image_path = os.path.join(IMAGE_DIR, image_file)
        convert_and_store_image(image_path)

    return JsonResponse({"status": "Images processed and stored in Redis"})
