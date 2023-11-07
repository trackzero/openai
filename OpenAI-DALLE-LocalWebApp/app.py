import os
from flask import Flask, session, request, render_template
import openai

app = Flask(__name__)
openai.api_key = os.environ.get("OPENAI_API_KEY")
app.secret_key = os.environ.get("FLASK_SECRET_KEY")

def generate_images(prompt, num_images):
    model = "dall-e-3" #was: "image-alpha-001"
    response_format = "url"
    size = "1024x1024"
    quality = "standard"
    images = openai.Image.create(model=model, prompt=prompt, response_format=response_format,
                                 num_images=num_images, size=size, quality=quality)
    urls = [img['url'] for img in images['data']]
    return urls

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        prompt = request.form["prompt"]
        num_images = int(request.form["num_images"])
        image_urls = generate_images(prompt, num_images)
        session["prompt"] = prompt
        return render_template("index.html", prompt=prompt, image_urls=image_urls)
    else:
        prompt = session.get("prompt", "")
        return render_template("index.html", prompt=prompt)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5050, debug=True)
