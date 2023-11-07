import os
from flask import Flask, session, request, render_template
from openai import OpenAI
client = OpenAI()

app = Flask(__name__)
client.api_key = os.environ.get("OPENAI_API_KEY")
app.secret_key = os.environ.get("FLASK_SECRET_KEY")

def generate_images(prompt, num_images):
    model = "dall-e-3" #was: "image-alpha-001"
    size="1024x1024"
    response = client.images.generate(model=model, prompt=prompt, n=num_images, size=size, quality="standard")
    
    urls = [data['url'] for data in response.data]
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
