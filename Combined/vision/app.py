from flask import Blueprint, render_template, request, send_from_directory, session, current_app
import os
import base64
from openai import OpenAI

vision_app = Blueprint('vision_app', __name__, template_folder='templates')

# Initialize the OpenAI client and set the API key
client = OpenAI()
client.api_key = os.getenv("OPENAI_API_KEY")

# Model name
model = "gpt-4-vision-preview"

# This session key stores the dialog history
SESSION_KEY_DIALOG_HISTORY = 'dialog_history'

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def reset_dialog_history():
    session[SESSION_KEY_DIALOG_HISTORY] = []

@vision_app.route("/")
def index():
    reset_dialog_history()  # Reset history whenever index is loaded
    return render_template("vision_index.html")

@vision_app.route('/uploads/<filename>')
def display_image(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)

@vision_app.route("/generate", methods=["POST"])
def generate_description():
    image = request.files.get("image")
    description_text = request.form.get("description_text", "What's in this image?")

    if image and image.filename != "":
        # If a new file is selected, save it as working_image.jpg
        image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'working_image.jpg')
        image.save(image_path)
    else:
        # If no new file is selected, continue using the existing working_image.jpg
        image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'working_image.jpg')

    base64_image = encode_image(image_path)

    # Store only the filename in the session, not the entire image content
    session[SESSION_KEY_DIALOG_HISTORY].append({
        "role": "system",
        "content": "User uploaded a new image." if image and image.filename != "" else "User continued with the existing image."
    })
    session[SESSION_KEY_DIALOG_HISTORY].append({
        "role": "user",
        "content": [
            {"type": "text", "text": description_text},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
        ],
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
    return render_template("vision_index.html", description=description, history=messages, image_uploaded=os.path.exists(image_path))

@vision_app.route("/reset", methods=["POST"])
def reset_session():
    reset_dialog_history()
    return render_template('vision_index.html', description='', history=[])
