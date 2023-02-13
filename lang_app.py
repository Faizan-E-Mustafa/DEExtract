import streamlit as st
import spacy
import pandas as pd

from main import VocabExtractor

nlp = spacy.load("de_core_news_sm")
vocab_ext = VocabExtractor()


@st.cache_data
def convert_df(df):
    return df.to_csv(index=False).encode("utf-8")


st.write(
    """
# Vocab Extractor
"""
)

query = st.text_input("Enter Text!", "")

if query != "":
    doc = nlp(query)
    extractions = []
    for sentence in doc.sents:
        extractions.extend(vocab_ext.extract_verbs(sentence))
    df = pd.DataFrame({"VERBS": extractions})

    st.dataframe(df)

    csv = convert_df(df)

    st.download_button(
        "Press to Download", csv, "file.csv", "text/csv", key="download-csv"
    )
