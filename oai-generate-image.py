import os
import openai
import requests
from requests.structures import CaseInsensitiveDict
import json
from PIL import Image
import requests
from io import BytesIO

#openai.organization = "org-placeholder"
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_image(prompt):
    model = "image-alpha-001"
    response_format = "url"
    num_images = 1
    size = "512x512"
    image = openai.Image.create(model=model, prompt=prompt, response_format=response_format,
                                 num_images=num_images, size=size)
    return image['data'][0]['url']

prompt = input("Enter a prompt: ")
image_url = generate_image(prompt)
print(image_url)

response = requests.get(image_url)
img = Image.open(BytesIO(response.content))
img.show()
