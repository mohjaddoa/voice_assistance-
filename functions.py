### this function return files path
import os
import tempfile
from langchain.document_loaders import PyPDFLoader
from langchain.document_loaders import Docx2txtLoader
from langchain.document_loaders import TextLoader
from langchain.vectorstores import chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain_community.chat_models import ChatOpenAI
import pysqlite3
import sys

sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

os.environ["OPENAI_API_KEY"] = "sk-proj-brqN4OAVd8oLBpIMI5RJT3BlbkFJAM1GDoUFx9FhQ4OPUSS8"

'''get_paths function take upload_files as input from
streamlit return list of files path'''
def get_paths(uploaded_files):
    files_path=[]
    for file in uploaded_files:
        file_name = file.name
        temp_dir = tempfile.mkdtemp()
        path = os.path.join(temp_dir, file_name)
        with open(path, "wb") as f:
            f.write(file.getvalue())
        files_path.append(path)
    return files_path

''' files_to_text function take path of files as input and return set of text'''
def files_to_text(paths):
    documents = []
    for file_path in paths:
        if file_path.endswith('.pdf'):
            loader = PyPDFLoader(file_path)
            documents.extend(loader.load())
        elif file_path.endswith('.docx') or file_path.endswith('.doc'):
            loader = Docx2txtLoader(file_path)
            documents.extend(loader.load())
        elif file_path.endswith('.txt'):
            loader = TextLoader(file_path)
            documents.extend(loader.load())
    return documents
''' text_spliter function spliting text to chungs'''
def text_spliter(set_text):
    text_spliter = CharacterTextSplitter(chunk_size=1000,chunk_overlap=100)
    text_doc = text_spliter.split_documents(set_text)
    return text_doc
    
''' text2vectors function take three parameters 
1-set of text
2- folder path
3- type of data embedding
return database of vectors , convert all text to numbers
and save it in database,and convert database as file
'''
def text2vectors(set_text,folder_path,data_embedding):
    if data_embedding == 'OpenAIEmbeddings':
        vectordb = chroma.Chroma.from_documents(set_text, embedding=OpenAIEmbeddings(), persist_directory=folder_path)
    vectordb.persist()
    return vectordb

def chat_with_llm(query,vector_data):
    chaining = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(),
    retriever=vector_data.as_retriever(search_kwargs={'k': 7}),
    return_source_documents=True)
    result = chaining({'query': query})
    response = result['result']
    return response
