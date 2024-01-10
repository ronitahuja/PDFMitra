from model import extract_text_from_pdf, bert
from chatmodel import fun
from grammarmodel import grammar_check_model
import streamlit as st

st.set_page_config(layout="wide")

def handleuser_input(user_question):
    response = st.session_state.conversation_chain({'question': user_question})
    st.session_state.chat_history = response['chat_history']
    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            with st.chat_message(name="user",avatar="https://www.freeiconspng.com/uploads/am-a-19-year-old-multimedia-artist-student-from-manila--21.png"):
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
                    summary=bert(extracted_text,slider_value)
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
                        summary=bert(extracted_text,slider_value)
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