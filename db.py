import chromadb
import streamlit as st
from config import CHROMA_PATH
 
@st.cache_resource
def get_db():
    return chromadb.PersistentClient(path=CHROMA_PATH)
 
client = get_db()
 
user_coll = client.get_or_create_collection("users")
chat_coll = client.get_or_create_collection("history")
feedback_coll = client.get_or_create_collection("feedback")