import streamlit as st

st.title("Home")
st.write("---")
col1, col2 = st.columns(2)

page1 = st.Page(r"page1.py", title="Mobile Network", icon=":material/share:")
page2 = st.Page(r"page2.py", title="Text2Panda Engine", icon=":material/description:")

with col1:
    st.write("Task 1: Mobile Network Geographical Area using LSTM")
    st.image("images/Online world-amico.png", caption="Takes the old day csv file and the current day csv file to predict feature11, and feature 12")
    st.page_link(page1, use_container_width=1)
with col2:
    st.write("Task 2: Text2Pandas Engine using LLM")
    st.write("  \n")
    st.image("images/Chat bot-pana.png", caption="Task 2: Text2Pandas Engine using LLM")
    st.page_link(page2, use_container_width=1)
st.write("---")