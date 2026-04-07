import uuid
from datetime import datetime
from db import feedback_coll

# from config import CSV_FEEDBACK_FILE
# import os,csv
# def save_to_csv(username, prompt, response):
#     file_exists = os.path.isfile(CSV_FEEDBACK_FILE)
#     with open(CSV_FEEDBACK_FILE, mode='a', newline='', encoding='utf-8') as f:
#         writer = csv.writer(f)
#         if not file_exists:
#             writer.writerow(["Timestamp", "Username", "Prompt", "Response"])
#         writer.writerow([datetime.now(), username, prompt, response])


def save_feedback(username, prompt, response):
    feedback_coll.add(
        ids=[str(uuid.uuid4())],
        documents=[response],
        metadatas=[{
            "username": username,
            "prompt": prompt,
            "timestamp": str(datetime.now())
        }]
    )

def handle_feedback(st):
    if st.session_state.messages and st.session_state.messages[-1]["role"] == "assistant":
        c1, c2 = st.columns([1, 8])
        # with c1:
        #     if st.button("👍"):
        #         save_to_csv(st.session_state.username, st.session_state.messages[-2]["content"], st.session_state.messages[-1]["content"])
        #         st.success("Saved!")
        with c1:
            if st.button("👍"):
            # Updated function call
                save_feedback(
                    st.session_state.username, 
                    st.session_state.messages[-2]["content"], #The last user question
                    st.session_state.messages[-1]["content"],#The last ai answer
                )
                st.success("Saved to Database!")
                

        with c2:
            if st.button("👎"):
                st.session_state.messages.pop() 
                st.session_state.retry_trigger = True
                st.rerun()