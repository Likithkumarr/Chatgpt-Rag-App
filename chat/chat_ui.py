import streamlit as st
import json
import uuid
from db import chat_coll
import time
from rag.rag_pipeline import build_rag
 
def render_sidebar():
 
    with st.sidebar:
        st.subheader(f"👤 {st.session_state.username}")
 
        # ---------------- CONTROL BUTTONS ----------------
        if st.button("➕ New Chat Session"):
            st.session_state.current_session_id = str(uuid.uuid4())
            st.session_state.messages = []
            st.rerun()
 
        if st.button("🧹 Clear Current Screen"):
            st.session_state.messages = []
            st.rerun()
 
        if st.button("🗑️ DELETE ALL MY HISTORY"):
            chat_coll.delete(where={"username": st.session_state.username})
            st.session_state.messages = []
            st.session_state.current_session_id = str(uuid.uuid4())
            st.warning("All history deleted forever!")
            st.rerun()
 
        if st.button("🚪 Logout"):
            st.session_state.clear()
            st.rerun()
 
        st.divider()
        # ---------------- FILE UPLOAD ----------------
        uploaded_files = st.file_uploader(
            "Upload Knowledge Files",
            accept_multiple_files=True
        )
        if uploaded_files:
            st.session_state.uploaded_filenames = [f.name for f in uploaded_files]
    
            if uploaded_files and not st.session_state.retriever:
                with st.status("🚀 Initializing Document Engine...", expanded=True) as s:
                    st.session_state.retriever = build_rag(uploaded_files)
                    st.write("📂 Reading uploaded files...")
                    # Simulate your file processing
                    time.sleep(1)

                    st.write("✂️ Splitting text into chunks...")
                    time.sleep(1)

                    st.write("🧠 Generating vector embeddings (Azure OpenAI)...")
                    time.sleep(1)

                    st.write("✅ Database persistence complete.")
                    s.update(label="✨ Indexing Complete!", state="complete",expanded=False)
        st.divider()
 
        # ---------------- CHAT HISTORY ----------------
        st.subheader("📜 Your Past Chats")
 
        user_chats = chat_coll.get(where={"username": st.session_state.username})
 
        if user_chats["ids"]:
            for i, sid in enumerate(user_chats["ids"]):
                title = user_chats["metadatas"][i].get("title", f"Chat {i}")
 
                if st.button(f"💬 {title[:15]}...", key=f"h_{sid}"):
                    st.session_state.current_session_id = sid
                    st.session_state.messages = json.loads(user_chats["documents"][i])
                    st.rerun()

        return uploaded_files