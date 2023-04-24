# openai
Experiments with the OpenAI API. You'll need your own API keys.


## Python
Start with `pip install openai`

### oai-generate-image.py
Your own personal command-line version of DALL-E. Can also wrap it in a flask script fairly easily; just ask ChatGPT for instructions.

Might need to `pip install pillow` on this one.

### oai-text-gen-with-secrets.py
ChatGPT from the command line, pull the API key from AWS Secrets Manager.  You have to have AWS auth env variables set up on your system to use this.

You'll need to `pip install aws-secretsmanager-caching` for this one. Oh, and `boto3` and `botocore`

### oai-text-gen.py
ChatGPT from the command line, but you just need your API key in the OPENAI_API_KEY environment variable.
