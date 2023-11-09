from flask import Flask, render_template, request, send_from_directory, session
import os
import base64
from openai import OpenAI

app = Flask(__name__)

# Initialize the OpenAI client and set the API key
client = OpenAI()
client.api_key = os.getenv("OPENAI_API_KEY")
app.secret_key = os.getenv("FLASK_SECRET_KEY")
app.config['UPLOAD_FOLDER'] = 'uploads'

# Model name
model = "gpt-4-vision-preview"

# This session key stores the dialog history
SESSION_KEY_DIALOG_HISTORY = 'dialog_history'

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def reset_dialog_history():
    session[SESSION_KEY_DIALOG_HISTORY] = []

@app.route("/")
def index():
    reset_dialog_history()  # Reset history whenever index is loaded
    return render_template("index.html")

@app.route('/uploads/<filename>')
def display_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route("/generate", methods=["POST"])
def generate_description():
    image = request.files.get("image")
    description_text = request.form.get("description_text", "What's in this image?")
    
    if image and image.filename != "":
        # Save the new image and add to dialog_history
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
        image.save(image_path)
        base64_image = encode_image(image_path)
        session[SESSION_KEY_DIALOG_HISTORY].append({
            "role": "system",
            "content": f"User uploaded a new image: {image.filename}"
        })
        session[SESSION_KEY_DIALOG_HISTORY].append({
            "role": "user",
            "content": [
                {"type": "text", "text": description_text},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
            ],
        })

    elif description_text:  # If no new image, but there is user input
        session[SESSION_KEY_DIALOG_HISTORY].append({
            "role": "user",
            "content": description_text
        })

    messages = session.get(SESSION_KEY_DIALOG_HISTORY, [])
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=300,
    )
    
    # after the response, add bot's response to history
    session[SESSION_KEY_DIALOG_HISTORY].append({
        "role": "assistant",
        "content": response.choices[0].message.content
    })
    
    description = response.choices[0].message.content
    return render_template("index.html", description=description, history=messages)

@app.route("/reset", methods=["POST"])
def reset_session():
    reset_dialog_history()
    return render_template('index.html', description='', history=[])

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5050, debug=True)