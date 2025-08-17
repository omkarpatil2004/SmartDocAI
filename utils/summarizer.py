from transformers import pipeline

# Abstractive summarization
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def abstractive_summary(text, max_len=150, min_len=40):
    summary = summarizer(text, max_length=max_len, min_length=min_len, do_sample=False)
    return summary[0]['summary_text']
