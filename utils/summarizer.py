from transformers import pipeline

# load summarizer once
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def chunk_text(text, max_tokens=900):
    """
    Splits text into smaller chunks for summarization.
    """
    words = text.split()
    for i in range(0, len(words), max_tokens):
        yield " ".join(words[i:i+max_tokens])

def abstractive_summary(text, max_len=200, min_len=50):
    """
    Summarize large text by chunking
    """
    chunks = list(chunk_text(text))
    summaries = []

    for chunk in chunks:
        try:
            summary = summarizer(
                chunk,
                max_length=max_len,
                min_length=min_len,
                do_sample=False
            )
            summaries.append(summary[0]['summary_text'])
        except Exception as e:
            summaries.append(f"[Error summarizing chunk: {e}]")

    # join all chunk summaries
    final_summary = " ".join(summaries)
    return final_summary
