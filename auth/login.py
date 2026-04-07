import streamlit as st
import time
from db import user_coll
 
def login():
    u = st.text_input("Username")
    p = st.text_input("Password", type="password")
 
    if st.button("Login"):
        res = user_coll.get(ids=[u])
 
        if res["ids"] and res["metadatas"][0]["pw"] == p:
 
            meta = res["metadatas"][0]
 
            st.session_state.logged_in = True
            st.session_state.username = u
 
            # 🔥 LOAD SAVED NAME (IMPORTANT)
            st.session_state.display_name = meta.get("name", u)
 
            st.success(f"✅ Welcome {st.session_state.display_name}")
            st.balloons()
            time.sleep(1)
            st.rerun()
 
        else:
            st.error("Invalid Credentials")