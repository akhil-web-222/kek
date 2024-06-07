import streamlit as st
import pandas as pd
import json
import os
import psutil
from streamlit.components.v1 import html
def read_file(filename):
  fh = open(filename, "r")
  try:
      return fh.read()
  finally:
      fh.close()
#from configparser
#global df
# Get the total memory capacity in bytes
total_memory = psutil.virtual_memory().total

# Convert the bytes to gigabytes
total_memory_gb = total_memory / (1024 * 1024 * 1024)

if total_memory_gb < float(20):

    # Define the error message
    error_message = "Insufficient Memory"

    # Display the error message using st.error()
    st.error(error_message, icon="❗️")  # You can add an icon (optional)

    # You can also add additional information below the error message
    st.write("Minimum Memory: 20GB")
    st.write(f"Device Memory: {round(total_memory_gb,2)}GB")
    try:
        import gpustat

        gpu_stats = gpustat.GPUStatCollection.new_query()

        for gpu in gpu_stats.gpus:
            print(f"GPU {gpu.index}: {gpu.name}, Memory: {gpu.memory_usage}")
    except:
        st.toast('Error: GPU not detected', icon='❗️')
else:
    import transformers
    import torch
    import json
    import streamlit as st
    model_id = "meta-llama/Meta-Llama-3-8B-Instruct"
    #model_id = "QuantFactory/Meta-Llama-3-8B-Instruct-GGUF"
    # tokenizer = AutoTokenizer.from_pretrained(model_id)
    # model = AutoModelForCausalLM.from_pretrained(
    #     model_id,
    #     torch_dtype=torch.bfloat16,
    #     device_map="auto",
    #     offload_folder="offload"
    # )
    @st.cache_resource
    def modelpipeline():
        pipeline = transformers.pipeline(
            "text-generation",
            model=model_id,
            model_kwargs={"torch_dtype": torch.bfloat16},
            device_map="auto",
            offload_folder="offload"
        )
        return pipeline
    file = open("/content/kek/schema.json","r")
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
    @st.cache_resource
    def data_to_json(data,schema=schema):
        messages = [
            {"role": "system", "content": f"""
                You are a Data Converter which can convert a given sample of data to JSON format using the following schema:
                {schema}
            """},
            {"role": "user", "content": f"Convert the following data into JSON: {data} and Strictly return the JSON data. No other additional data is required"},
        ]
        pipeline = modelpipeline()
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
            max_new_tokens=3000,
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
                max_new_tokens=3000,
                eos_token_id=terminators,
                do_sample=True,
                temperature=0.6,
                top_p=0.9,
            )
            print(outputs[0]["generated_text"][len(prompt):])
            response = outputs[0]["generated_text"][len(prompt):]
        return response
    

    #from apis.filter_api import data_to_json, json_corrector
    
    
    def validate_json(json_string):
        """Validates the provided JSON string and returns a formatted preview."""
        try:
            json_data = json.loads(json_string)
            formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
            st.success("JSON is valid!")
            st.code(formatted_json, language="json")
            print(os.getcwd())
        except json.JSONDecodeError as e:
            st.error(f"Invalid JSON: {e}")
    @st.cache_resource
    def filter_data(df, schema, num_rows):
        """Performs data filtering based on uploaded file, schema, and number of rows."""
        df = df#pd.read_csv(file)

        # Apply schema if provided
        if schema:
            try:
                schema_dict = json.loads(schema)
                # Implement filtering logic based on schema (e.g., type checks, value ranges)
                # ... (You'll need to customize this part based on your specific schema format)
            except json.JSONDecodeError:
                st.error("Invalid JSON schema")
                return

        # Filter by number of rows
        if num_rows > 0:
            df = df.head(num_rows)

        # Handle output format
        if st.session_state["output_format"] == "JSON":
            # Convert dataframe to JSON
            #json_data = df.to_json(orient="records")
            json_filtered_data = list()
            for index,row in df.iterrows():
                if index < num_rows:
                    data = data_to_json(row,schema)
                    json_filtered_data.append(data)
                else:
                    break
            write_to_text_file(json_filtered_data,"filtered-json-data.txt")
            write_json_list_to_file(json_filtered_data,"filtered-json-data.json")      
            st.success("Data filtered and converted to JSON:")
            with open("filtered-json-data.txt","r") as text:
                text_data = text.read()
                st.code(text_data, language="json")
            text.close()
        else:
            # Write filtered dataframe to CSV
            st.download_button("Download CSV", df.to_csv(index=False), file_name="filtered_data.csv")

    st.title("Data Filter")

    # Upload CSV file
    uploaded_file = st.file_uploader("Upload CSV file:", type="csv")
    if uploaded_file is not None:
        #global df
        df = pd.read_csv(uploaded_file)
        st.success("CSV file uploaded!")
        st.write(df.head())

    # Number of rows to filter
    num_rows = st.number_input("Number of rows to filter (0 for all)", min_value=0)

    # Schema section
    st.header("Schema (Optional)")
    schema = st.text_area("Enter JSON schema (if applicable)", height=200)
    if schema:
        validate_json_button = st.button("Validate JSON")
        if validate_json_button:
            validate_json(schema)

    # Output format
    st.header("Output Format")
    output_format = st.selectbox("Choose output format", ("JSON", "CSV"))
    st.session_state["output_format"] = output_format

    # Define column details for CSV
    if output_format == "CSV":
        num_columns = st.number_input("Number of columns in CSV", min_value=1)
        if num_columns > 0:
            column_names = []
            column_descriptions = []
            for i in range(num_columns):
                column_names.append(st.text_input(f"Column Name {i+1}"))
                column_descriptions.append(st.text_input(f"Column Description {i+1} (Optional)", key=i))

    # Filter button
    if st.button("Filter Data"):
        # Run long-duration function
        filter_data(df, schema, num_rows)

        
