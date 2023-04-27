import os
import json
import openai
from colorama import init, Fore, Style
import botocore
import botocore.session
from botocore.exceptions import ClientError
from aws_secretsmanager_caching import SecretCache, SecretCacheConfig 

model="gpt-3.5-turbo"     #"gpt-4" if you have it.

# Retrieve API key from AWS Secrets Manager, or try environment variable
def get_secret():
    secret_name = "openai_api_key"
    region_name = "us-west-2"

    # Create boto client/session
    try:
        client = botocore.session.get_session().create_client('secretsmanager', region_name=region_name)
        cache_config = SecretCacheConfig()
        cache = SecretCache( config = cache_config, client = client)

        # Retrieve secret and cache
        secret = cache.get_secret_string(secret_name)
        secret_dict = json.loads(secret)

        return secret_dict['openai_api_key']
    except ClientError as e:
        # Print error if secret retrieval fails
        print(Fore.YELLOW + f"Error retrieving secret: {e}" + Style.RESET_ALL)
        # Try environment variable instead
        openai_api_key = os.environ.get('OPENAI_API_KEY')
        if openai_api_key:
            print(Fore.YELLOW + "Trying environment variable instead of AWS Secrets Manager" + Style.RESET_ALL)
            return openai_api_key
        else:
            print(Fore.RED + "Environment variable OPENAI_API_KEY not found" + Style.RESET_ALL)

# Set up initial conversation context
conversation = []

# Set up colorama
init()

# Create an instance of the ChatCompletion API
def chatbot(conversation):
    max_tokens=1024
    try:
        response= openai.ChatCompletion.create(
            model=model,
            messages=conversation,
            max_tokens=max_tokens,
            stream=True)
        
        #event variables
        collected_chunks=[]
        collected_messages = ""

        #capture and print event stream
        print(Fore.YELLOW + "Bot: " + Style.RESET_ALL)
        for chunk in response:
            collected_chunks.append(chunk)  # save the event response
            chunk_message = chunk['choices'][0]['delta']  # extract the message
            if "content" in chunk_message:
                message_text = chunk_message['content']
                collected_messages += message_text
                print(f"{message_text}", end="")
        print(f"\n")
        return(collected_messages)
    except Exception as e:
        # Print error if chatbot fails to generate response
        print(Fore.RED + f"Error generating chat response: {e}" + Style.RESET_ALL)

# Print welcome message and instructions
print(Fore.GREEN + "Welcome to the chatbot! To start, enter your message below.")
print("To reset the conversation, type 'reset' or 'let's start over'.")
print("To stop, say 'stop','exit', or 'bye'" + Style.RESET_ALL)

# Loop to continuously prompt user for input and get response from OpenAI
while True:
    try:
        user_input = input(Fore.CYAN + "User: " + Style.RESET_ALL)
        if user_input.lower() in ["reset", "let's start over"]:
            conversation = []
            print(Fore.YELLOW + "Bot: Okay, let's start over." + Style.RESET_ALL)

        elif user_input.lower() in ["stop", "exit", "bye", "quit", "goodbye"]:
            print(Fore.RED + Style.BRIGHT + "Bot: Okay, goodbye!" + Style.RESET_ALL)
            break
        else:
            # Append user message to conversation context
            conversation.append({"role": "user", "content": user_input})
            # Generate chat completion
            chat = chatbot(conversation)

            # Append bot message to conversation context
            conversation.append({"role": "assistant", "content": chat})
    except KeyboardInterrupt:
        # Handle keyboard interrupt gracefully
        print(Fore.RED + Style.BRIGHT + "Bot: Okay, goodbye!" + Style.RESET_ALL)
        break
    except Exception as e:
        # Print error if an unexpected exception occurs
        print(Fore.RED + f"Unexpected error: {e}" + Style.RESET_ALL)