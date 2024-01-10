import google.generativeai as genai
import dotenv
import os

def grammar_check_model(input_text):
    dotenv.load_dotenv()
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    
    model=genai.GenerativeModel('gemini-pro')
    model=model.start_chat(history=[])
    command='''You should act like a experienced english teacher. Your work is to check the 
    grammatical mistakes in the given text and then output the corrected text. Your text is....'''
    response=model.send_message(command+input_text)
    
    return response.text

if __name__=='__main__':
    grammar_check_model()