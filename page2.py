import streamlit as st
from langchain_google_genai import GoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain


st.title('Task 2: Text2Pandas Engine')

def create_chain(API):
    prompt = PromptTemplate(input_variables=['query'],
          template="""you are a helpfull AI assistant with main task to take human query and convert it to pandas code by Python to apply on DataFram

your response should give the pandas code that solve the human question 
%Note%: you must answer by only Python code without explanation

given the dataset column names list = ['cell_no', 'hour', 'month', 'day', 'year', 'Bandwidth', 'counter_0',
       'counter_1', 'counter_2', 'counter_3', 'counter_4', 'counter_5']

given that the DataFrame is named as df

Question Example: What is the maximum value for counter_2 for all of the cells?
Expected Output: df['counter_2'].max()

%Note%: your response will path on eval python function, so you need to only write python commands without any character else
%Note%: never ever type other letter except the commands

You are developed by Eng. Abdallah Fekry

%Query%: {query}
""")
    llm = GoogleGenerativeAI(model="gemini-1.5-flash",google_api_key=API,temprature=0)
    chain = LLMChain(llm=llm, prompt=prompt)
    return chain

API = "AIzaSyBIvw7QEbrnN7HJTBqxu6CI_r7egCWf5tU"

if 'chain' not in st.session_state:
    st.session_state.chain = create_chain(API)

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.chat_message('assistant').markdown("Hello how can i help you today!")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Write your query"):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    response = st.session_state.chain.run(prompt)
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
