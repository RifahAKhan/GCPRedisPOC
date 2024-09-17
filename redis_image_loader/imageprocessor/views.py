# views.py
from django.shortcuts import render
import os
from PIL import Image
from django.http import JsonResponse
from django.conf import settings
import logging

# Set up logging
logger = logging.getLogger(__name__)

# Redis instance from settings.py
redis_instance = settings.redis_instance

# Directory where the images will be mounted
IMAGE_DIR = '/images'

def convert_and_store_image(image_path):
    try:
        # Open the image file
        with Image.open(image_path) as img:
            # Convert to 6-bit
            img = img.convert('P', palette=Image.ADAPTIVE, colors=64)
            # Save the image to a temporary location in memory
            temp_path = f'/tmp/{os.path.basename(image_path)}'
            img.save(temp_path, 'PNG')

            # Read the file into memory and store it in Redis
            with open(temp_path, 'rb') as f:
                redis_instance.set(f"image:{os.path.basename(image_path)}", f.read())
            logger.info(f"Image {image_path} processed and stored in Redis")
    except Exception as e:
        logger.error(f"Error processing image {image_path}: {e}")

def load_images_to_redis(request):
    try:
        image_files = os.listdir(IMAGE_DIR)
        logger.info(f"Found {len(image_files)} images in {IMAGE_DIR}")

        for image_file in image_files:
            image_path = os.path.join(IMAGE_DIR, image_file)
            convert_and_store_image(image_path)

        return JsonResponse({"status": "Images processed and stored in Redis"})
    except Exception as e:
        logger.error(f"Error loading images to Redis: {e}")
        return JsonResponse({"status": "Error", "message": str(e)}, status=500)