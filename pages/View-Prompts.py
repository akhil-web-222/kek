import streamlit as st
import importlib

# Function to load prompts.py and update variables
def update_prompts(new_chat_prompt, new_json_converter_prompt, new_json_validator_prompt):
  prompts = importlib.import_module("apis.prompts")
  prompts.chat_system_prompt = new_chat_prompt
  prompts.json_converter_prompt = new_json_converter_prompt
  prompts.json_validator_prompt = new_json_validator_prompt

  # Save the changes to prompts.py (implement your preferred save method)
  # This example just prints for demonstration - implement actual saving logic
  print(f"Updated prompts: chat_system: {prompts.chat_system_prompt}, json_converter: {prompts.json_converter_prompt}, json_validator: {prompts.json_validator_prompt}")

st.title("Edit Prompts")

# Load initial values from prompts.py (implement your preferred loading method)
# This example assumes prompts.py is directly accessible
prompts = importlib.import_module("apis.prompts")
chat_system_prompt = prompts.chat_system_prompt
json_converter_prompt = prompts.json_converter_prompt
json_validator_prompt = prompts.json_validator_prompt

# Text input fields for editing variables
new_chat_prompt = st.text_input("Chat System Prompt", chat_system_prompt)
new_json_converter_prompt = st.text_input("JSON Converter Prompt", json_converter_prompt)
new_json_validator_prompt = st.text_input("JSON Validator Prompt", json_validator_prompt)

# Save button to trigger update function
if st.button("Save Changes"):
  update_prompts(new_chat_prompt, new_json_converter_prompt, new_json_validator_prompt)
  st.success("Prompts updated successfully (implementation for saving needed)!")

