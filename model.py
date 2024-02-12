import PyPDF2
from transformers import BartTokenizer, BartForConditionalGeneration
import torch

def extract_text_from_pdf(pdf_file):
    text = ""
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    for page_num in range(len(pdf_reader.pages)):
        text+=pdf_reader.pages[page_num].extract_text()
    return text
def bart(text,max_size):
    model_name = "facebook/bart-large-cnn"
    tokenizer = BartTokenizer.from_pretrained(model_name)
    model = BartForConditionalGeneration.from_pretrained(model_name)
    def summarize():
        if text:
            chunk_size = 1024
            overlap = 200
            text_segments = []
            for i in range(0, len(text), chunk_size - overlap):
                segment = text[i:i + chunk_size]
                text_segments.append(segment)

            summaries = []
            previous_summary = None

            for segment in text_segments:
                input_ids = tokenizer.encode(segment, return_tensors="pt", max_length=1024, truncation=True)
                if previous_summary is not None:
                    input_ids = torch.cat([previous_summary, input_ids], dim=1)

                summary_ids = model.generate(input_ids, max_length=max_size, min_length=30, length_penalty=2.0, num_beams=4, early_stopping=False)
                summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
                summaries.append(summary)
                previous_summary = summary_ids

            full_summary = "\n".join(summaries)

            return full_summary
    return summarize()