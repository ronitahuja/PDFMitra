from model import extract_text_from_pdf, bart
from chatmodel import fun
from grammarmodel import grammar_check_model
import streamlit as st

st.set_page_config(layout="wide")

def handleuser_input(user_question):
    response = st.session_state.conversation_chain({'question': user_question})
    st.session_state.chat_history = response['chat_history']
    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            with st.chat_message(name="user",avatar="data:image/png;base64,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"):
                st.write(message.content)
        else:
            with st.chat_message(name="assistant",avatar="https://i.ibb.co/cN0nmSj/Screenshot-2023-05-28-at-02-37-21.png"):
                st.write(message.content)
            
def summarize(uploaded_file,input_text):
    with st.spinner("In progress"):
        extracted_text=""
        if uploaded_file is not None :extracted_text=extract_text_from_pdf(uploaded_file)
        else : extracted_text=input_text

        slider_value = st.slider("Select a value:", min_value=1, max_value=len(extracted_text.split()), value=5, step=1)

        if uploaded_file:
            if st.button('summarize'):
                col1, col2 = st.columns(2)
                with col1:
                    st.info("Extracted Text")
                    st.write(extracted_text)
                with col2:
                    summary=bart(extracted_text,slider_value)
                    st.info("Summarization Complete")
                    st.success(summary)
                st.info("chat with pdf")
                st.write(fun(extracted_text))
        else:
            if input_text:
                if st.button("Summarize"):
                    col1, col2 = st.columns(2)
                    if(input_text==""): return
                    with col1:
                        st.info("Input Text")
                        st.write(input_text)
                    with col2:
                        summary=bart(extracted_text,slider_value)
                        st.info("Summarization Complete")
                        st.success(summary)
                    
def question_and_ans(uploaded_file,input_text):
    with st.spinner("In progress"):
        extracted_text=""
        if uploaded_file is not None :extracted_text=extract_text_from_pdf(uploaded_file)
        else : extracted_text=input_text
        user_question=st.text_area("Enter your question")
        if st.button("process"):
            conversation_chain=fun(extracted_text)
            st.session_state.conversation_chain=conversation_chain
            handleuser_input(user_question)
            
def grammar_check(uploaded_file,input_text):
    with st.spinner("In progress"):
        extracted_text=""
        if uploaded_file is not None: extracted_text=extract_text_from_pdf(uploaded_file)
        else : extracted_text=input_text
        col1,col2=st.columns(2)
        with col1:
            st.info("Original text")
            st.write(extracted_text)
        with col2:
            st.info("Corrected text")
            st.write(grammar_check_model(extracted_text))
    
    
    
def main():
    selected_section=""
    section_options=[
        "Summarize",
        "Q/A with PDF",
        "Grammar Check"
    ]
    with st.sidebar:
        st.subheader("select file")
        uploaded_file = st.file_uploader("Upload your PDF file", type=['pdf'])
        input_text=st.text_area("Enter your text")
        if(uploaded_file or input_text):
            st.sidebar.title("Summarizar OR QA with PDF")
            select_box_placeholder = st.sidebar.empty()
            selected_section = select_box_placeholder.selectbox("Select Task", section_options)
    if selected_section == "Summarize":
        summarize(uploaded_file,input_text)
    elif selected_section=="Q/A with PDF":
        question_and_ans(uploaded_file,input_text)
    elif selected_section=="Grammar Check":
        grammar_check(uploaded_file,input_text)
    
    
if __name__ =="__main__":
    main()