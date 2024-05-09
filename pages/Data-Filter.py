import streamlit as st
import pandas as pd
import json
import os
import psutil
#global df
# Get the total memory capacity in bytes
total_memory = psutil.virtual_memory().total

# Convert the bytes to gigabytes
total_memory_gb = total_memory / (1024 * 1024 * 1024)

if total_memory_gb > float(20):

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
    import dotenv
    dotenv.load_dotenv()
    import os
    access_token_read = os.getenv('HF_TOKEN')
    #from apis.filter_api import data_to_json
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
            json_data = df.to_json(orient="records")
            i=0
            for index, row in df.iterrows():
                if i<num_rows:
                    # Convert the row to a list
                    list_row = row.tolist()
                    #print(list_row)
                    #print("Next row")
                    #if my_filter(list_row):
                    #    print(f"Row {index+1} passed the filter: {list_row}") 
                    data_to_json(schema,str(list_row))
                    i+=1
                else:
                    break
            st.success("Data filtered and converted to JSON:")
            st.code(json_data, language="json")
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
        filter_data(df, schema, num_rows)