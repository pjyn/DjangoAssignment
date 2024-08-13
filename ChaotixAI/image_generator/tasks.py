from celery import shared_task
import requests
from django.conf import settings
import os

API_HOST = os.getenv('API_HOST', 'https://api.stability.ai')

@shared_task
def generate_image(prompt):
    url = f"{API_HOST}/v1/generation/stable-diffusion-v1-6/text-to-image"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {settings.STABILITY_AI_API_KEY}",
    }
    data = {
        "text_prompts": [
            {"text": prompt}
        ],
        "cfg_scale": 7,
        "height": 1024,
        "width": 1024,
        "samples": 1,
        "steps": 30,
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        
        response_data = response.json()
        image_data = response_data.get("artifacts", [])
        
        if not image_data:
            return ("", "", "No images returned")
        
        # Assuming we need to handle one image
        image = image_data[0]
        image_base64 = image.get("base64", "")
        return (image_base64, "", "")
    
    except requests.RequestException as e:
        return ("", "", f"Error: {str(e)}")
    