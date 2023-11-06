import os
import openai
openai.organization = "org-1wAvzL2IG2n8DfJ9213Yvkdv"
openai.api_key = os.getenv("OPENAI_API_KEY")
response = openai.Model.list()
models = response["data"]

for model in models:
	model_id = model["id"]
	print(model_id)