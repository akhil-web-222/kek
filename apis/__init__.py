import os
import sys
import dotenv

from .rag_api import rag_api
from .filter_api import filter_api




file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)
dotenv.load_dotenv()
access_token_read = os.getenv('HUGGINGFACE_TOKEN')