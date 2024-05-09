from transformers import AutoTokenizer, AutoModelForCausalLM, AutoConfig, pipeline
from time import time
import transformers
import torch
from prompts import *
from langchain.llms import HuggingFacePipeline
try:
  from langchain_community.document_loaders import JSONLoader
except:
  from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma
import dotenv
dotenv.load_dotenv()
import os
access_token_read = os.getenv('HF_TOKEN')

# Loading Model and Tokenizer
model_checkpoint = 'meta-llama/Meta-Llama-3-8B-Instruct'
model_config = AutoConfig.from_pretrained(model_checkpoint, trust_remote_code=True, max_new_tokens=1024, use_auth_token=True)

model = AutoModelForCausalLM.from_pretrained(model_checkpoint, trust_remote_code=True, config=model_config, device_map='auto', use_auth_token=True)

tokenizer = AutoTokenizer.from_pretrained(model_checkpoint, use_auth_token=True)

# Pipeline Creation
pipeline = pipeline("text-generation", model=model, tokenizer=tokenizer, torch_dtype=torch.float16, max_length=3000, device_map="auto")

llm = HuggingFacePipeline(pipeline=pipeline)

# Parsing function
def parse(string):
        return string.split("<|end_header_id|>")[-1]

# Retriever
try:
  loader = JSONLoader("/data/data.json")
except:
  loader = PyPDFLoader("/data/data.pdf")
documents = loader.load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_documents(documents)

embedding_function = SentenceTransformerEmbeddings(model_name="BAAI/bge-small-en-v1.5")
vectorstore = Chroma(collection_name="sample_collection", embedding_function = embedding_function)

vectorstore.add_documents(texts)

retriever = vectorstore.as_retriever(k=7)

# Pipeline Object
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
    
pipe = Pipeline(llm,retriever)

def chat(prompt):
    if(prompt is not None):
        output = pipe.generate(prompt)
        return output