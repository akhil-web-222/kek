import streamlit as st
from st_chat_message import message
#from streamlit_chat import message
from streamlit.components.v1 import html
from huggingface_hub import login
hutoken = "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"
login(token=hutoken)
def read_file(filename):
  fh = open(filename, "r")
  try:
      return fh.read()
  finally:
      fh.close()
import os
import sys
import psutil
print("This is the current working directory: ",os.getcwd())
from transformers import AutoTokenizer, AutoModelForCausalLM, AutoConfig, pipeline
from time import time
import transformers
import torch
chat_system_prompt = """
    You are an advanced assistant that always greets users with catchy taglines for making them buy products named Galaxy AI made for people visiting the Samsung India website.
    You can help them find offers for devices, suggest devices based on their requirements, budget etc.
    While displaying any offer related information, give the response in a tabular markdown format with columns Sr No, Offer, Provider, Offer amount and Final price of device after offer (calculate as per requirement).
    If the user tries to ask out of topic questions do not engange in the conversation.
    If the given context is not sufficient to answer the question,Do not answer the question.
    This is the season of Diwali. So always give them wishes for that in a fancy way.
"""
from langchain.llms import HuggingFacePipeline
try:
  from langchain_community.document_loaders import JSONLoader, TextLoader
except:
  from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.llms import HuggingFacePipeline

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
    #from apis.rag_api import chat
    @st.cache_resource
    def llm():
        # Loading Model and Tokenizer
        model_checkpoint = 'meta-llama/Meta-Llama-3-8B-Instruct'
        model_config = AutoConfig.from_pretrained(model_checkpoint, trust_remote_code=True, max_new_tokens=1024, use_auth_token=True)

        model = AutoModelForCausalLM.from_pretrained(model_checkpoint, trust_remote_code=True, config=model_config, device_map='auto', use_auth_token=True)

        tokenizer = AutoTokenizer.from_pretrained(model_checkpoint, use_auth_token=True)

        # Pipeline Creation
        pipy = pipeline("text-generation", model=model, tokenizer=tokenizer, torch_dtype=torch.float16, max_length=3000, device_map="auto")

        llmpipe = HuggingFacePipeline(pipeline=pipy)
        return llmpipe
    # Parsing function
    def parse(string):
            return string.split("<|end_header_id|>")[-1]

    
    # Retriever
    @st.cache_resource
    def retriever():
        try:
            loader = JSONLoader("/content/CorrectedData.json")
        except:
            loader = TextLoader("/content/Alldata.txt")
        documents = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        texts = text_splitter.split_documents(documents)

        embedding_function = SentenceTransformerEmbeddings(model_name="BAAI/bge-small-en-v1.5")
        vectorstore = Chroma(collection_name="sample_collection", embedding_function = embedding_function)

        vectorstore.add_documents(texts)

        retrieverdata = vectorstore.as_retriever(k=7)
        return retrieverdata
    
    # Pipeline Object
    # @st.cache_resource
    class Pipeline:
        def __init__(self,llm,retriever):
            self.llm = llm
            self.retriever = retriever
        def retrieve(self,question):
            docs = self.retriever.invoke(question)
            return "\n\n".join([d.page_content for d in docs])
        # You are a helpful, respectful and honest Sales assistant for Samsung that is made to give answers regarding offers for Samsung Products.
        #            If the user asks for offers on any phone, give the offers in a tabular format with columns: Offer Provider, Offer Type, Offer Amount, Minimum Purchase Value, Offer Description, Final Price after offer (calculated accordingly).
        #            The response should be given in Markdown format.
        #            If the user tries to ask out of topic questions do not engange in the conversation.
        #            If the given context is not sufficient to answer the question,Do not answer the question.
        def augment(self,question,context):
            return f"""
                <|begin_of_text|>
                <|start_header_id|>
                system
                <|end_header_id|>
                {chat_system_prompt}
                <|eot_id|>
                <|start_header_id|>
                user
                <|end_header_id|>
                Answer the user question based on the context provided below
                Context :{context}
                Question: {question}
                <|eot_id|>
                <|start_header_id|>
                assistant
                <|end_header_id|>"""
        def parse(self,string):
            return string.split("<|end_header_id|>")[-1]
        def generate(self,question):
            context = self.retrieve(question)
            prompt  = self.augment(question,context)
            answer  = self.llm.invoke(prompt)
            return self.parse(answer)
    # @st.cache_resource    
    def pipe():    
        piped = Pipeline(llm(),retriever())
        return piped
    def chat(prompt):
        if(prompt is not None):
            output = pipe().generate(prompt)
            return output
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
                "content":"Hi, I am Galaxy AI",
                "is_user":False,
            },
        ]
    chat_placeholder = st.empty()

    with chat_placeholder.container():
        for idx, msg in enumerate(st.session_state.msgs):
            message(msg["content"], is_user=msg["is_user"], key=f"message_{idx}")
    

    with st.container():
        st.text_input("Request:", on_change=on_input_change, key="user_input")
        # create st.empty() container
