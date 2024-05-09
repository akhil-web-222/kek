import os
import sys

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)
from .rag_api import rag_api
from .filter_api import filter_api

import dotenv
dotenv.load_dotenv()
import os
access_token_read = os.getenv('HUGGINGFACE_TOKEN')