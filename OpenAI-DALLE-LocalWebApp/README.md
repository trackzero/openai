Basic Flask app to run against DALL-E 3.

run "python app.py" and then browse to localhost:5050.

Or you can run the dockerfile and set it up in a container.  I'm running mine
on a Synology NAS; you'll have to go into the container & populate the env vars
with your flask secret & OpenAI API keys.