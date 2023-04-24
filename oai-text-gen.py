import os
import openai
from colorama import init, Fore, Style

#openai.organization = "org-placeholder"
openai.api_key = os.getenv("OPENAI_API_KEY")
model="gpt-3.5-turbo"     #"gpt-4"

# Set up initial conversation context
conversation = []

# init colorama
init()

# Create an instance of the ChatCompletion API
def chatbot(conversation):
    max_tokens=1024
    completion= openai.ChatCompletion.create(model=model, messages=conversation, max_tokens=max_tokens)
    return completion["choices"][0]["message"]["content"]

# Print welcome message and instructions
print(Fore.GREEN + "Welcome to the chatbot! To start, enter your message below.")
print("To reset the conversation, type 'reset' or 'let's start over'.")
print("To stop, say 'stop','exit', or 'bye'" + Style.RESET_ALL)

# Loop to continuously prompt user for input and get response from OpenAI
while True:
    user_input = input(Fore.CYAN + "User: " + Style.RESET_ALL)
    if user_input.lower() in ["reset", "restart", "let's start over"]:
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

        # Print response
        print(Fore.YELLOW + "Bot: " + Style.RESET_ALL + chat)