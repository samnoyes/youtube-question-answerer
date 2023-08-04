import os
import openai
import sys
sys.path.append('../..')

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

openai.api_key  = os.environ['OPENAI_API_KEY']

from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings

if len(sys.argv) < 3:
    print("Error: You must provide a vector store dir and a question as a command-line argument.")
    print("Usage: python answer_question.py <name_of_vector_store> <question>")
    sys.exit()

save_dir=sys.argv[1]
persist_directory = f'docs/chroma/{save_dir}'
embedding = OpenAIEmbeddings()
vectordb = Chroma(
    persist_directory=persist_directory,
    embedding_function=embedding
)
question = sys.argv[2]
# docs_ss = vectordb.similarity_search(question,k=3)

from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI

llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

qa_chain = RetrievalQA.from_chain_type(
    llm,
    retriever=vectordb.as_retriever()
)

result = qa_chain({"query": question})

print(result["result"])