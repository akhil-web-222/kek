import streamlit as st
from st_chat_message import message
#from streamlit_chat import message
from streamlit.components.v1 import html

import os
import sys
import psutil

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
    import dotenv
    dotenv.load_dotenv()
    import os
    access_token_read = os.getenv('HUGGINGFACE_TOKEN')
    from apis.rag_api import chat
    def on_input_change():
        user_input = st.session_state.user_input
        print(repr(user_input))
        if len(user_input) == 0:
            return None
        st.session_state.msgs.append({"content":str(user_input),"is_user":True})
        value = chat(user_input)
        st.session_state.msgs.append({"content":str(value),"is_user":False})
        
    if "msgs" not in st.session_state:
        st.session_state.msgs = [
            {
                "content":"Hi, Hariharan",
                "is_user":False,
            },
        ]
    chat_placeholder = st.empty()

    with chat_placeholder.container():
        for idx, msg in enumerate(st.session_state.msgs):
            message(msg["content"], is_user=msg["is_user"], key=f"message_{idx}")


    with st.container():
        st.text_input("Request:", on_change=on_input_change, key="user_input")