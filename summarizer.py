# Optimized summarizer.py

import streamlit as st
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

# Small, fast, and reliable model
MODEL_NAME = "t5-small"

# -------------------------------
# Load model once (cached)
# -------------------------------
@st.cache_resource
def load_model():
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
    return tokenizer, model

# -------------------------------
# Summarization Function
# -------------------------------
def summarize(text, short=False):
    if not text:
        return "No content available to summarize."

    tokenizer, model = load_model()

    input_text = "summarize: " + text
    inputs = tokenizer(
        input_text,
        return_tensors="pt",
        truncation=True,
        max_length=512
    )

    max_tokens = 60 if short else 140

    with torch.no_grad():
        outputs = model.generate(
            inputs["input_ids"],
            max_new_tokens=max_tokens,
            do_sample=False
        )

    summary = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return summary
