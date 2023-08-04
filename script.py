import os
import openai
import sys
sys.path.append('../..')

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

openai.api_key  = os.environ['OPENAI_API_KEY']

from langchain.chat_models import ChatOpenAI
from langchain.document_loaders.generic import GenericLoader
from langchain.document_loaders.parsers import OpenAIWhisperParser
from langchain.document_loaders.blob_loaders.youtube_audio import YoutubeAudioLoader

if len(sys.argv) < 3:
    print("Error: You must provide a YouTube link and a vector store name as a command-line argument.")
    print("Usage: python script.py <youtube_link> <directory_of_vector_store>")
    sys.exit()

url = sys.argv[1]
save_dir=sys.argv[2]
youtube_dir=f"docs/youtube/{save_dir}"
loader = GenericLoader(
    YoutubeAudioLoader([url],youtube_dir),
    OpenAIWhisperParser()
)
docs = loader.load()

from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter

r_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=100,
    separators=["\n\n", "\n", "(?<=\. )", " ", ""]
)
splits = r_splitter.split_text(docs[0].page_content)

from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
embedding = OpenAIEmbeddings()
persist_directory = f'docs/chroma/{save_dir}'
vectordb = Chroma.from_texts(
    texts=splits,
    embedding=embedding,
    persist_directory=persist_directory
)

vectordb.persist()