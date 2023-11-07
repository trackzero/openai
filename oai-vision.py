import os
import base64
from openai import OpenAI
client=OpenAI()

#openai.organization = "org-placeholder"
client.api_key = os.getenv("OPENAI_API_KEY")
model="gpt-4-vision-preview"

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Path to your image
image_path = "assets/sample.jpg"

# Getting the base64 string
base64_image = encode_image(image_path)

response = client.chat.completions.create(
	model=model,
	messages = [
		{
            "role": "user",
            "content": [
                {"type": "text", "text": "What’s in this image?"},
                {
                    "type": "image_url",
                    "image_url": {
                    	"url": f"data:image/jpeg;base64,{base64_image}"
                    },
                },
            ],
        }
    ],
    max_tokens=300,
    )

print(response.choices[0])