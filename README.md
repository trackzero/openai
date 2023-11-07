# openai
Experiments with the OpenAI API. You'll need your own API keys.  Define 'em in the
**OPENAI_API_KEY** environment variable.

There is little to no error handling, that's just how I roll.

## Python
Latest update, I was running Python 3.11

You'll want to start with `pip install openai`; most of these have been brought up to v1.1.1 (Nov 6 2023)

### oai-generate-image.py
Your own personal command-line version of DALL-E 3. (Might need to `pip install pillow` on the CLI version)

For more flexibility, use the Flask app under `OpenAI-DALLE-LocalWebApp`

Here's a screenshot:

![Screenshot of the Flask app](assets/cyber-crow.png)

I even included a dockerfile if you want to try to run it in a container.  I don't know what I'm doing but I got it to work.

The Flask app will currently persist your prompt, but not the other settings. It's a bug. Maybe I'll fix it, maybe I won't.

### oai-text-gen.py
ChatGPT from the command line, but you just need your API key in the OPENAI_API_KEY environment variable.

### oai-text-gen-with-secrets.py
ChatGPT from the command line, but pull the API key from AWS Secrets Manager.  You have to have AWS auth env variables set up on your system to use this. Uses Secrets Manager Caching where applicable.

You'll need to `pip install aws-secretsmanager-caching` for this one. Oh, and `boto3` and `botocore`

### oai-text-gen-with-secrets-and-streaming.py
Added streaming responses into the mix.
**NOTE** this one has not been updated for the OpenAI library v1.1.1 so it doesn't work without some virtualenv muddling.  Prob still works if you're running OpenAI library 0.27.4 or thereabouts, but everything else will throw errors.


