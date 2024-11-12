from flask import Flask, render_template, request, send_from_directory, session, url_for, jsonify
import os
import base64
import mimetypes
from openai import OpenAI
from pydub import AudioSegment

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
from openai import Audio

app = Flask(__name__)

# Set the OpenAI API key
app.secret_key = os.getenv("FLASK_SECRET_KEY")
app.config['UPLOAD_FOLDER'] = 'uploads'

# Model name
model = "gpt-4o"
imgmodel = "dall-e-3"

# This session key stores the dialog history
SESSION_KEY_DIALOG_HISTORY = 'dialog_history'
SESSION_KEY_IMAGE_HISTORY = 'image_history'

image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'working_image.jpg')

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def reset_dialog_history():
    session[SESSION_KEY_DIALOG_HISTORY] = []
    session[SESSION_KEY_IMAGE_HISTORY] = []

def generate_images(prompt, size, style, quality):
    response = client.images.generate(model=imgmodel,
    prompt=prompt,
    size=size,
    style=style,
    quality=quality)

    image_url = response.data[0].url
    return image_url

# Helper function to split audio files
def split_audio_file(file_path, max_size=25 * 1024 * 1024):
    # Determine the audio format based on the file extension
    mime_type, _ = mimetypes.guess_type(file_path)
    audio_format = mime_type.split('/')[1] if mime_type else 'wav'

    # Load the audio file with the correct format
    audio = AudioSegment.from_file(file_path, format=audio_format)
    audio_size = os.path.getsize(file_path)
    
    # If the audio file is within the size limit, return the original file
    if audio_size <= max_size:
        return [file_path]
    
    # Calculate number of chunks needed
    num_chunks = (audio_size // max_size) + 1
    chunk_duration_ms = len(audio) / num_chunks  # Duration in milliseconds
    
    # Split the audio into chunks and export them
    audio_chunks = []
    for i in range(num_chunks):
        start_time = i * chunk_duration_ms
        end_time = start_time + chunk_duration_ms
        chunk = audio[start_time:end_time]
        chunk_path = f"{file_path}_chunk_{i}.mp3"  # Export as mp3 for compatibility
        chunk.export(chunk_path, format="mp3")
        audio_chunks.append(chunk_path)
    
    return audio_chunks


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/vision")
def vision_index():
    reset_dialog_history()  # Reset history whenever index is loaded
    return render_template("vision_index.html")

@app.route('/uploads/<filename>')
def display_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route("/generate", methods=["POST"])
def generate_description():
    image = request.files.get("image")
    description_text = request.form.get("description_text", "What's in this image?")

    if image and image.filename != "":
        # If a new file is selected, save it as working_image.jpg
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'working_image.jpg')
        image.save(image_path)
    else:
        # If no new file is selected, continue using the existing working_image.jpg
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'working_image.jpg')

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

    # Store the image in the image history
    session.setdefault(SESSION_KEY_IMAGE_HISTORY, []).append(base64_image)

    messages = session.get(SESSION_KEY_DIALOG_HISTORY, [])
    response = client.chat.completions.create(model=model,
    messages=messages,
    max_tokens=300)

    # after the response, add bot's response to history
    session[SESSION_KEY_DIALOG_HISTORY].append({
        "role": "assistant",
        "content": response.choices[0].message.content
    })

    description = response.choices[0].message.content
    cache_buster = os.path.getmtime(image_path) if os.path.exists(image_path) else 0
    return render_template("vision_index.html", description=description, history=messages, image_uploaded=os.path.exists(image_path), cache_buster=cache_buster)

@app.route("/reset", methods=["POST"])
def reset_session():
    reset_dialog_history()
    return render_template('vision_index.html', description='', history=[])

@app.route("/dalle", methods=["GET", "POST"])
def dalle_index():
    if request.method == "POST":
        prompt = request.form.get("prompt")
        size = request.form.get("size")
        style = request.form.get("style")
        quality = request.form.get("quality")
        image_url = generate_images(prompt, size, style, quality)
        session.setdefault(SESSION_KEY_IMAGE_HISTORY, []).append(image_url)
        session["prompt"] = prompt
        session["size"] = size
        session["style"] = style
        session["quality"] = quality

        return render_template("dalle_index.html", prompt=prompt, size=size, style=style, quality=quality, image_url=image_url, history=session.get(SESSION_KEY_IMAGE_HISTORY, []))
    else:
        prompt = session.get("prompt", "")
        size = session.get("size", "1024x1024")
        style = session.get("style", "vivid")
        quality = session.get("quality", "standard")
        return render_template("dalle_index.html", prompt=prompt, history=session.get(SESSION_KEY_IMAGE_HISTORY, []))

@app.route("/audio", methods=["GET", "POST"])
def audio_to_text():
    if request.method == "POST":
        audio_file = request.files.get("audio")
        if audio_file:
            # Get the original filename and extension
            filename = audio_file.filename
            extension = os.path.splitext(filename)[1].lower()
            
            # Ensure the uploaded file has one of the supported extensions
            supported_extensions = ['.mp3', '.mp4', '.mpeg', '.mpga', '.m4a', '.wav', '.webm']
            if extension not in supported_extensions:
                return render_template("audio_index.html", error="Unsupported audio format.")
            
            # Save the uploaded audio file with its original extension
            audio_path = os.path.join(app.config['UPLOAD_FOLDER'], f'uploaded_audio{extension}')
            audio_file.save(audio_path)
    
            # Use the split_audio_file function to get the list of audio files (chunks)
            audio_files = split_audio_file(audio_path)
    
            transcripts = []
    
            for chunk_path in audio_files:
                with open(chunk_path, "rb") as audio_chunk:
                    response = client.audio.transcriptions.create(model="whisper-1", file=audio_chunk)
                    transcripts.append(response.text)
                # Clean up chunk files except the original
                if chunk_path != audio_path:
                    os.remove(chunk_path)
    
            # Concatenate all transcripts
            full_transcript = ' '.join(transcripts)
    
            return render_template("audio_index.html", transcript=full_transcript)
    
    return render_template("audio_index.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5050, debug=True)
