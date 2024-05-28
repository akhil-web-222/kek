import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, AutoConfig


# Import required libraries
import json
from transformers import AutoTokenizer, AutoModelForCausalLM, AutoConfig
from time import time
import transformers
import torch
from transformers import pipeline
from transformers import AutoTokenizer
from transformers import BitsAndBytesConfig
from huggingface_hub import login
import dotenv
dotenv.load_dotenv()
import os
access_token_read = os.getenv('HF_TOKEN')
login(token = access_token_read)

# Set up model and tokenizer
if torch.cuda.get_device_capability()[0] >= 8:
    attn_implementation = "flash_attention_2"
    torch_dtype = torch.bfloat16
else:
    attn_implementation = "eager"
    torch_dtype = torch.float16


#model_checkpoint = 'meta-llama/Meta-Llama-3-8B-Instruct'
#model_checkpoint = 'microsoft/Phi-3-medium-128k-instruct'
model_checkpoint = 'C:\MicroLLM\gemma_2b_it'
model_config = AutoConfig.from_pretrained(model_checkpoint, trust_remote_code=True, max_new_tokens=1024, use_auth_token=True)
model = AutoModelForCausalLM.from_pretrained(model_checkpoint, trust_remote_code=True, config=model_config, device_map='auto', use_auth_token=True)
tokenizer = AutoTokenizer.from_pretrained(model_checkpoint, use_auth_token=True)

def json_corrector(json,schema):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = model.to(device)
    prompt = f"""The given json object has some errors with it. Rectify those errors based on the JSON Format and strictly give me the JSON response and nothing else:

JSON:
{json}

JSON Format:
{schema}"""

    inputs = tokenizer(prompt, return_tensors="pt").to(device)
    output_ids = model.generate(**inputs, max_new_tokens=3000, temperature=0.7)
    output = tokenizer.batch_decode(output_ids, skip_special_tokens=True)[0]
    return output

# Define the generation function
def data_to_json(schema, content):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = model.to(device)
    prompt = f"""Change the following text to the specified JSON format:

Text:
{content}

JSON Format:
{schema}"""

    inputs = tokenizer(prompt, return_tensors="pt").to(device)
    output_ids = model.generate(**inputs, max_new_tokens=3000, temperature=0.7)
    output = tokenizer.batch_decode(output_ids, skip_special_tokens=True)[0]
    return output
