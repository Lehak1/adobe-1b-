import nltk
from nltk.tokenize import sent_tokenize
import heapq
import re

# Ensure NLTK sentence tokenizer is available
try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt")

def clean_text(text):
    """
    Basic cleaning: removes extra spaces and special characters.
    """
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def score_sentences(text, top_n=3):
    """
    Scores sentences based on keyword frequency (naive extractive summarizer).
    """
    sentences = sent_tokenize(text)
    if len(sentences) <= top_n:
        return sentences  # Not enough to summarize

    # Word frequency
    freq = {}
    for sentence in sentences:
        for word in sentence.lower().split():
            freq[word] = freq.get(word, 0) + 1

    # Score each sentence
    sentence_scores = []
    for sentence in sentences:
        words = sentence.lower().split()
        if not words:
            continue
        score = sum(freq.get(word, 0) for word in words) / (len(words) + 1e-6)
        sentence_scores.append((score, sentence))

    # Get top-N scored sentences
    top_sentences = heapq.nlargest(top_n, sentence_scores)
    return [sentence for _, sentence in top_sentences]

def summarize(text, max_sentences=3):
    """
    Extractive summary: returns the top N most relevant sentences.
    """
    cleaned = clean_text(text)
    top_sents = score_sentences(cleaned, top_n=max_sentences)
    return " ".join(top_sents)

def refine_section_text(text):
    """
    Wrapper for summarizing a section before ranking.
    """
    return summarize(text, max_sentences=3)
