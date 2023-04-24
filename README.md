# openai
Experiments with the OpenAI API. You'll need your own API keys.

There is little to no error handling, that's not how I roll.

## Python
Start with `pip install openai`

### oai-generate-image.py
Your own personal command-line version of DALL-E. Can also wrap it in a flask script fairly easily; just ask ChatGPT for instructions, it spit out a page that worked for me.

Might need to `pip install pillow` on this one.

### oai-text-gen.py
ChatGPT from the command line, but you just need your API key in the OPENAI_API_KEY environment variable.

### oai-text-gen-with-secrets.py
ChatGPT from the command line, pull the API key from AWS Secrets Manager.  You have to have AWS auth env variables set up on your system to use this. Uses Secrets Manager Caching where applicable.

You'll need to `pip install aws-secretsmanager-caching` for this one. Oh, and `boto3` and `botocore`

### oai-text-gen-with-secrets-and-streaming.py
Added streaming responses into the mix.


