import streamlit as st
from client.agent_client import run_agent_query

st.title("🧠 SQLite Agent UI")
user_input = st.text_input("Ask something:", "")

if st.button("Submit") and user_input:
    with st.spinner("Thinking..."):
        response = run_agent_query(user_input)
        st.markdown("**Response:**")
        st.write(response)
