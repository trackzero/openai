import os
from flask import Flask, session, request, render_template
from openai import OpenAI
client = OpenAI()

app = Flask(__name__)
client.api_key = os.environ.get("OPENAI_API_KEY")
app.secret_key = os.environ.get("FLASK_SECRET_KEY")

def generate_images(prompt, size, style, quality):
    model = "dall-e-3"  # Adjust the model name if needed
    response = client.images.generate(
        model=model,
        prompt=prompt,
        size=size,
        style=style,
        quality=quality,
    )

    image_url = response.data[0].url
    return image_url

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        prompt = request.form.get("prompt")
        size = request.form.get("size")
        style = request.form.get("style")
        quality = request.form.get("quality")
        image_url = generate_images(prompt, size, style, quality)
        session["prompt"] = prompt
        session["size"] = size
        session["style"] = style
        session["quality"] = quality

        return render_template("index.html", prompt=prompt, size=size, style=style, quality=quality, image_url=image_url)
    else:
        prompt = session.get("prompt", "")
        size = session.get("size", "1024x1024")
        style = session.get("style", "vivid")
        quality = session.get("quality", "standard")
        return render_template("index.html", prompt=prompt)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5050, debug=True)
