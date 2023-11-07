from flask import Flask, render_template, request
import os
import base64
from openai import OpenAI

app = Flask(__name__)

# Initialize the OpenAI client and set the API key
client = OpenAI()
client.api_key = os.getenv("OPENAI_API_KEY")
app.secret_key=os.getenv("FLASK_SECRET_KEY")

# Model name
model = "gpt-4-vision-preview"

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/", methods=["POST"])
def generate_description():
    if "image" in request.files:
        image = request.files["image"]
        if image.filename != "":
            image_path = "path_to_save_image.jpg"  # Specify the path to save the uploaded image
            image.save(image_path)

            # Encode the image and generate the description (similar to your existing code)
            base64_image = encode_image(image_path)
            response = client.chat.completions.create(
                model=model,
                messages=[
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
            description = response.choices[0].message.content

            return render_template("index.html", description=description)
        else:
            return "No file selected"
    else:
        return "Invalid request"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5050, debug=True)

