import transformers
import torch
import json
model_id = "meta-llama/Meta-Llama-3-8B-Instruct"
#model_id = "QuantFactory/Meta-Llama-3-8B-Instruct-GGUF"
# tokenizer = AutoTokenizer.from_pretrained(model_id)
# model = AutoModelForCausalLM.from_pretrained(
#     model_id,
#     torch_dtype=torch.bfloat16,
#     device_map="auto",
#     offload_folder="offload"
# )

pipeline = transformers.pipeline(
    "text-generation",
    model=model_id,
    model_kwargs={"torch_dtype": torch.bfloat16},
    device_map="auto",
    offload_folder="offload"
)

file = open("schema.json","r")
schema = file.read()
print(schema)

def write_json_list_to_file(data, filename):
    """
    This function writes a list of JSON strings (objects) to a file, one per line.

    Args:
        data: A list of strings representing JSON objects.
        filename: The name of the file to write to (str).
    """
    with open(filename, 'w') as f:
        for item in data:
            try:
                # Validate JSON data (optional)
                json.loads(item)
                f.write(item + '\n')  # Add newline after each valid JSON object
            except json.JSONDecodeError:
                print(f"WARNING: Skipping invalid JSON object: {item}")
    f.close()
def write_to_text_file(data, filename):
    """
    This function writes a list of JSON strings (objects) to a text file, one per line even if they're not JSON compatible.

    Args:
        data: A list of strings representing JSON objects.
        filename: The name of the file to write to (str).
    """
    with open(filename, 'w') as f:
        for item in data:
            f.write(item)
            f.write("\n")
    f.close()

def is_valid_json(data):
    """
    This function checks if the given data is valid JSON format.

    Args:
        data: The data to be checked (str).

    Returns:
        True if the data is valid JSON, False otherwise.
    """
    try:
        json.loads(data)
    except (json.JSONDecodeError, TypeError) as e:
        return False
    return True

def data_to_json(data,schema=schema):
    messages = [
        {"role": "system", "content": f"""
            You are a Data Converter which can convert a given sample of data to JSON format using the following schema:
            {schema}
        """},
        {"role": "user", "content": f"Convert the following data into JSON: {data} and Strictly return the JSON data. No other additional data is required"},
    ]

    prompt = pipeline.tokenizer.apply_chat_template(
        messages, 
        tokenize=False, 
        add_generation_prompt=True
    )

    terminators = [
        pipeline.tokenizer.eos_token_id,
        pipeline.tokenizer.convert_tokens_to_ids("<|eot_id|>")
    ]

    outputs = pipeline(
        prompt,
        max_new_tokens=256,
        eos_token_id=terminators,
        do_sample=True,
        temperature=0.6,
        top_p=0.9,
    )

    print(outputs[0]["generated_text"][len(prompt):])
    response = outputs[0]["generated_text"][len(prompt):]
    #print(tokenizer.decode(response, skip_special_tokens=True))
    if is_valid_json(response):
        return response
    else:
        messages.append({"role":"assistant","content":f"{response}"})
        messages.append({"role":"user","content":f"Strictly follow the schema {schema} and give the response in JSON object. No other additional conversation is required."})
        # input_ids = tokenizer.apply_chat_template(
        #     messages,
        #     add_generation_prompt=True,
        #     return_tensors="pt"
        # ).to(model.device)

        # terminators = [
        #     tokenizer.eos_token_id,
        #     tokenizer.convert_tokens_to_ids("<|eot_id|>")
        # ]

        # outputs = model.generate(
        #     input_ids,
        #     max_new_tokens=256,
        #     eos_token_id=terminators,
        #     do_sample=True,
        #     temperature=0.6,
        #     top_p=0.9,
        # )
        # response = outputs[0][input_ids.shape[-1]:]        
        prompt = pipeline.tokenizer.apply_chat_template(
            messages, 
            tokenize=False, 
            add_generation_prompt=True
        )

        terminators = [
            pipeline.tokenizer.eos_token_id,
            pipeline.tokenizer.convert_tokens_to_ids("<|eot_id|>")
        ]

        outputs = pipeline(
            prompt,
            max_new_tokens=256,
            eos_token_id=terminators,
            do_sample=True,
            temperature=0.6,
            top_p=0.9,
        )
        print(outputs[0]["generated_text"][len(prompt):])
        response = outputs[0]["generated_text"][len(prompt):]
    return response