import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, AutoConfig


# Import required libraries
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
access_token_read = os.getenv('HUGGINGFACE_TOKEN')
login(token = access_token_read)

# Set up model and tokenizer
if torch.cuda.get_device_capability()[0] >= 8:
    attn_implementation = "flash_attention_2"
    torch_dtype = torch.bfloat16
else:
    attn_implementation = "eager"
    torch_dtype = torch.float16

access_token_read = "xyz"
login(token=access_token_read)

model_checkpoint = 'meta-llama/Meta-Llama-3-8B-Instruct'
model_config = AutoConfig.from_pretrained(model_checkpoint, trust_remote_code=True, max_new_tokens=1024)
model = AutoModelForCausalLM.from_pretrained(model_checkpoint, trust_remote_code=True, config=model_config, device_map='auto')
tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)


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
    output_ids = model.generate(**inputs, max_new_tokens=3000, temperature=0.0)
    output = tokenizer.batch_decode(output_ids, skip_special_tokens=True)[0]
    return output
