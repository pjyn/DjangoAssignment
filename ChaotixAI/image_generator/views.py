# from django.shortcuts import render

from django.http import JsonResponse
from .tasks import generate_image

def generate_images(request):
    prompts = ["A red flying dog", "A piano ninja", "A footballer kid"]
    
    # Launch tasks
    tasks = [generate_image.delay(prompt) for prompt in prompts]
    
    # Collect results
    results = []
    for task in tasks:
        try:
            result = task.get(timeout=10)  # Adjust timeout as needed
            image_base64, _, error = result
            if error:
                results.append({"error": error})
            else:
                results.append({"image_base64": image_base64})
        except Exception as e:
            results.append({"error": str(e)})
    
    return JsonResponse(results, safe=False)

