'''import streamlit as st
import os
import json
import pandas as pd

def get_directory_contents(path):
    """Gets the directories and files within a given path."""
    try:
        contents = os.listdir(path)
        directories = [os.path.join(path, d) for d in contents if os.path.isdir(os.path.join(path, d))]
        files = [os.path.join(path, f) for f in contents if os.path.isfile(os.path.join(path, f))]
        return directories, files
    except FileNotFoundError:
        return [], []

def view_file_content(file_path):
    """Views the content of a file based on its extension."""
    extension = os.path.splitext(file_path)[1].lower()
    if extension == '.json':
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            st.json(data)
        except json.JSONDecodeError:
            st.error(f"Error: Could not parse JSON file: {file_path}")
    elif extension == '.csv':
        try:
            df = pd.read_csv(file_path)
            st.dataframe(df)
        except pd.errors.ParserError:
            st.error(f"Error: Could not parse CSV file: {file_path}")
    else:
        st.write(f"Unsupported file type: {extension}")

def upload_and_preview_file(initial_path):
    """Uploads a new JSON or CSV file and displays a preview."""
    uploaded_file = st.file_uploader("Upload a JSON or CSV file", type=['json', 'csv'])
    if uploaded_file is not None:
        file_name = uploaded_file.name
        file_path = os.path.join(initial_path, file_name)
        try:
            with open(file_path, "wb") as f:
                f.write(uploaded_file.read())
            st.success(f"File '{file_name}' uploaded successfully!")
            view_file_content(file_path)
        except Exception as e:
            st.error(f"Error uploading file: {e}")

def main():
    """Main function to run the Streamlit app."""
    initial_path = st.text_input("Enter the desired directory path (or leave blank for current directory)", value="")
    if not initial_path:
        initial_path = os.getcwd()  # Use current working directory if not provided

    directories, files = get_directory_contents(initial_path)

    st.header("Directory Contents")
    st.write("Directories:")
    for directory in directories:
        st.write(directory)

    st.write("Files:")
    for file in files:
        st.write(file)
        if st.button(f"View {os.path.basename(file)} content"):
            view_file_content(file)

    upload_and_preview_file(initial_path)

if __name__ == "__main__":
    main()'''
##############################################################
# import streamlit as st
# import os
# import json
# import pandas as pd

# def get_directory_structure(path):
#     """Recursively retrieves directory structure with file types."""
#     try:
#         structure = {"type": "directory", "name": path, "children": []}
#         for item in os.listdir(path):
#             item_path = os.path.join(path, item)
#             if os.path.isfile(item_path):
#                 structure["children"].append({"type": "file", "name": item})
#             else:
#                 structure["children"].append(get_directory_structure(item_path))
#         return structure
#     except FileNotFoundError:
#         return None

# def display_tree(structure, indent=0):
#     """Displays directory structure in a tree view."""
#     if structure is None:
#         return
#     st.write(" " * indent + structure["name"])
#     if structure["type"] == "directory":
#         for child in structure["children"]:
#             display_tree(child, indent + 2)

# def view_file_content(path):
#     """Displays file content in a code block."""
#     try:
#         with open(path, "r") as file:
#             content = file.read()
#             st.code(content, language="text")
#     except FileNotFoundError:
#         st.error("File not found.")

# def upload_and_preview(path):
#     """Uploads JSON/CSV file and displays preview."""
#     uploaded_file = st.file_uploader("Upload file (JSON or CSV)", type=["json", "csv"])
#     if uploaded_file is not None:
#         try:
#             if uploaded_file.name.endswith(".json"):
#                 data = json.load(uploaded_file)
#                 st.subheader("JSON Preview")
#                 st.json(data)
#             elif uploaded_file.name.endswith(".csv"):
#                 data = pd.read_csv(uploaded_file)
#                 st.subheader("CSV Preview (limited to 10 rows)")
#                 st.dataframe(data.head(10))
#             else:
#                 st.warning("Unsupported file type. Please upload JSON or CSV.")
#         except json.JSONDecodeError:
#             st.error("Invalid JSON format.")

# # Get current working directory
# current_path = os.getcwd()

# # Display directory tree
# st.header("Directory Structure")
# directory_structure = get_directory_structure(current_path)
# display_tree(directory_structure)

# # Select directory or file
# selected_item = st.selectbox("Select an item", [item["name"] for item in directory_structure["children"] if item["type"] != "directory"])

# # View file content or upload new file
# if selected_item in [item["name"] for item in directory_structure["children"] if item["type"] == "file"]:
#     view_file_content(os.path.join(current_path, selected_item))
# else:
#     upload_and_preview(os.path.join(current_path, selected_item))

##########################################################
# import streamlit as st
# import os
# import json
# import pandas as pd

# # Function to recursively traverse directory structure and build tree view
# def get_directory_tree(data_dir):
#     tree = {}
#     for item in os.listdir(data_dir):
#         item_path = os.path.join(data_dir, item)
#         if os.path.isfile(item_path):
#             tree[item] = None  # Mark files as leaves in the tree
#         else:
#             tree[item] = get_directory_tree(item_path)  # Recursively explore subdirectories
#     return tree

# # Function to display tree view with appropriate indentation
# def display_tree(tree, level=0):
#     for item, children in tree.items():
#         indent = "  " * level
#         st.write(f"{indent}{item}")
#         if children:
#             display_tree(children, level + 1)

# # Function to display file content (JSON or CSV)
# def display_file_content(file_path):
#     if file_path.endswith(".json"):
#         with open(file_path, "r") as f:
#             try:
#                 data = json.load(f)
#                 st.json(data)
#             except json.JSONDecodeError:
#                 st.error("Invalid JSON format")
#     elif file_path.endswith(".csv"):
#         try:
#             df = pd.read_csv(file_path)
#             st.dataframe(df)
#         except pd.errors.ParserError:
#             st.error("Invalid CSV format")
#     else:
#         st.error("Unsupported file format")

# # Main app logic
# st.title("Directory Explorer and File Viewer")

# data_dir = os.path.join(os.getcwd(),"data")  # Replace with the actual directory path
# print(data_dir)
# # Check if the data directory exists
# if not os.path.exists(data_dir):
#     st.error(f"Directory '{data_dir}' does not exist.")
#     st.stop()

# # Get directory tree structure
# tree = get_directory_tree(data_dir)

# # Display directory tree view
# st.header("Directory Structure")
# display_tree(tree)

# # File upload section
# uploaded_file = st.file_uploader("Upload a JSON or CSV file", type=["json", "csv"])

# if uploaded_file is not None:
#     file_name = uploaded_file.name
#     file_path = os.path.join(data_dir, file_name)

#     # Save uploaded file
#     with open(file_path, "wb") as f:
#         f.write(uploaded_file.getbuffer())

#     # Display preview of uploaded file content
#     st.header("Preview of Uploaded File")
#     display_file_content(file_path)

# import streamlit as st
# import os
# import json
# import pandas as pd
# from streamlit_tree_select import tree_select  # Install using `pip install streamlit_tree_select`

# # Function to recursively traverse directory structure and build tree data
# def get_directory_tree(data_dir):
#     tree = []
#     for item in os.listdir(data_dir):
#         item_path = os.path.join(data_dir, item)
#         if os.path.isfile(item_path):
#             tree.append({"label": item, "is_file": True})
#         else:
#             tree.append({"label": item, "children": get_directory_tree(item_path)})
#     return tree

# # Function to display file content (limited preview for large files)
# def display_file_content(file_path):
#     if file_path.endswith(".json"):
#         with open(file_path, "r") as f:
#             try:
#                 data = json.load(f)
#                 st.json(data[:5])  # Display first 5 lines
#             except json.JSONDecodeError:
#                 st.error("Invalid JSON format")
#     elif file_path.endswith(".csv"):
#         try:
#             df = pd.read_csv(file_path, nrows=5)  # Read only first 5 rows
#             st.dataframe(df)
#         except pd.errors.ParserError:
#             st.error("Invalid CSV format")
#     else:
#         st.error("Unsupported file format")

# # Main app logic
# st.title("Directory Explorer and File Viewer")

# data_dir = "data"  # Replace with the actual directory path

# # Check if the data directory exists
# if not os.path.exists(data_dir):
#     st.error(f"Directory '{data_dir}' does not exist.")
#     st.stop()

# # Get directory tree structure
# tree_data = get_directory_tree(data_dir)

# # Display directory tree view using streamlit_tree_select
# selected_key = StreamlitTreeSelect(key="directory_tree", options=tree_data)

# # Check if a node (file) is selected
# if selected_key:
#     file_path = os.path.join(data_dir, selected_key.split("/")[-1])  # Extract file path from selected key

#     # Display preview of selected file content
#     st.header(f"Preview of '{file_path}'")
#     display_file_content(file_path)

# # File upload section
# uploaded_file = st.file_uploader("Upload a JSON or CSV file", type=["json", "csv"])

# if uploaded_file is not None:
#     file_name = uploaded_file.name
#     file_path = os.path.join(data_dir, file_name)

#     # Save uploaded file
#     with open(file_path, "wb") as f:
#         f.write(uploaded_file.getbuffer())
##############################################
# import streamlit as st
# import os
# import json
# import pandas as pd

# # Function to recursively traverse directory structure and display tree view
# def display_tree(data_dir, level=0):
#     for item in os.listdir(data_dir):
#         item_path = os.path.join(data_dir, item)
#         indent = "  " * level
#         st.write(indent + item)
#         if os.path.isfile(item_path):
#             # Indicate file with a marker (e.g., '*')
#             st.write(indent + "*")
#         else:
#             # Recursively explore subdirectories
#             display_tree(item_path, level + 1)

# # Function to display file content (limited preview for large files)
# def display_file_content(file_path):
#     if file_path.endswith(".json"):
#         with open(file_path, "r") as f:
#             try:
#                 data = json.load(f)
#                 st.json(data[:5])  # Display first 5 lines
#             except json.JSONDecodeError:
#                 st.error("Invalid JSON format")
#     elif file_path.endswith(".csv"):
#         try:
#             df = pd.read_csv(file_path, nrows=5)  # Read only first 5 rows
#             st.dataframe(df)
#         except pd.errors.ParserError:
#             st.error("Invalid CSV format")
#     else:
#         st.error("Unsupported file format")

# # Main app logic
# st.title("Directory Explorer and File Viewer")

# data_dir = os.path.join(os.getcwd(),"data")  # Replace with the actual directory path

# # Check if the data directory exists
# if not os.path.exists(data_dir):
#     st.error(f"Directory '{data_dir}' does not exist.")
#     st.stop()

# # Display directory tree view
# st.header("Directory Structure")
# display_tree(data_dir)

# # Selected file path (initially None)
# selected_file_path = None

# # User interaction for selecting a file
# user_input = st.text_input("Enter a file name (or path) to view:", "")

# # Check if user input matches an existing file
# if user_input:
#     for root, _, files in os.walk(data_dir):
#         for file in files:
#             if user_input == file or user_input == os.path.join(root, file):
#                 selected_file_path = os.path.join(root, file)
#                 break  # Stop searching after finding a match

# # Display preview of selected file content (if any)
# if selected_file_path:
#     st.header(f"Preview of '{selected_file_path}'")
#     display_file_content(selected_file_path)

# # File upload section
# uploaded_file = st.file_uploader("Upload a JSON or CSV file", type=["json", "csv"])

# if uploaded_file is not None:
#     file_name = uploaded_file.name
#     file_path = os.path.join(data_dir, file_name)

#     # Save uploaded file
#     with open(file_path, "wb") as f:
#         f.write(uploaded_file.getbuffer())
##################################################
import streamlit as st
import os
import json
import pandas as pd

# Function to recursively traverse directory structure and display with buttons
def display_tree(data_dir, level=0):
    for item in os.listdir(data_dir):
        item_path = os.path.join(data_dir, item)
        indent = "  " * level
        st.write(indent + item)
        if os.path.isfile(item_path):
            # Button for displaying file content
            if st.button(f"{indent}*{item}"):
                display_file_content(item_path)
        else:
            # Recursively explore subdirectories with a button
            if st.button(f"{indent}{item}"):
                display_tree(item_path, level + 1)

# Function to display file content (limited preview for large files)
def display_file_content(file_path):
    if file_path.endswith(".json"):
        with open(file_path, "r") as f:
            try:
                data = json.load(f)
                st.json(data[:5])  # Display first 5 lines
            except json.JSONDecodeError:
                st.error("Invalid JSON format")
    elif file_path.endswith(".csv"):
        try:
            df = pd.read_csv(file_path, nrows=5)  # Read only first 5 rows
            st.dataframe(df)
        except pd.errors.ParserError:
            st.error("Invalid CSV format")
    else:
        st.error("Unsupported file format")

# Main app logic
st.title("Directory Explorer and File Viewer")

data_dir = os.path.join(os.getcwd(),"data")  # Replace with the actual directory path

# Check if the data directory exists
if not os.path.exists(data_dir):
    st.error(f"Directory '{data_dir}' does not exist.")
    st.stop()

# Display directory tree view with buttons
st.header("Directory Structure")
display_tree(data_dir)

# File upload section
uploaded_file = st.file_uploader("Upload a JSON or CSV file", type=["json", "csv"])

if uploaded_file is not None:
    file_name = uploaded_file.name
    file_path = os.path.join(data_dir, file_name)

    # Save uploaded file
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.header("Preview of Uploaded File")
    display_file_content(file_path)