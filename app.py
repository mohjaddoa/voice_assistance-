import streamlit as st
import os
import tempfile
from functions import get_paths,files_to_text,text_spliter,text2vectors,chat_with_llm
from voice_recognition import get_audio,speech
import sys
import time 
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
## title
st.markdown("<h1 style='text-align: center;'>AI Voice Assistant</h1>", unsafe_allow_html=True)

image_path = 'https://moh2006.000webhostapp.com/images/sarah.jpg'

html_code = f"""
<div style="display: flex; justify-content: center;">
    <img src="{image_path}" alt="Centered Image" style="width: 300px; height: 300px;">
</div>
"""

# Display the HTML with the image
st.markdown(html_code, unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'>Now, you can talk with your files:PDF,DOCX,TXT</h1>", unsafe_allow_html=True)
# Custom CSS to center the link
st.markdown(
    """
    <style>
    .centered-link {
        display: flex;
        justify-content: center;
        align-items: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Create a container with the centered-link class
st.markdown(
    """
    <div class="centered-link">
        <a href="https://github.com/mohjaddoa/talk_2_files/" target="_blank">https://github.com/mohjaddoa/talk_2_files/</a>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("<br>", unsafe_allow_html=True)
# selecting multiple files
uploaded_files = st.file_uploader("Choose files: PDF,DOCX,TXT", accept_multiple_files=True,type=['pdf', 'txt', 'docx'])
# voice_button=st.button("voice query")
## this is loop for saveing all files content on temp,and get fils path
if uploaded_files:
    paths = get_paths(uploaded_files)
    # st.write(paths)
    set_text = files_to_text(paths)
    text_spliting = text_spliter(set_text)
    vector_data = text2vectors(text_spliting,'documents','OpenAIEmbeddings')
    with st.spinner('processing ....'):
        time.sleep(5)
    st.markdown("<h3 style='text-align: center;'>enter your query : by voice </h3>", unsafe_allow_html=True)
    query = st.text_input("enter your query ...")
    # voice_button=st.button("voice query",disabled=False)    
    if query :
        voice_button=st.button("voice query",disabled=True)
        chat_response = chat_with_llm(query,vector_data)
        with st.spinner('processing ....'):
            time.sleep(5)
        status='response:'
        st.write(status)
        st.write(chat_response)
    else:
        voice_button=st.button("voice query",disabled=False)
        query=""
        if voice_button:
            speech('This is Sarah AI Voice Assistant , How can I help You?')
            while(True):
                text_voice = get_audio()
                # text_voice += "chatgpt, ask me several clarifying questions that help you get better context"
                if(text_voice == "stop" or text_voice == "close"):
                    st.write("stop voice conversation..." )
                    sys.exit()
                else:
                    st.write("your query :"+text_voice)
                    st.spinner('query processing ....')
                    chat_response = chat_with_llm(text_voice,vector_data)
                    status='AI response:'
                    st.write(status)
                    st.write(chat_response)
                    speech(chat_response)
                    speech(" IF you want continue ask more question , or quit by saying stop or close")







    
 
