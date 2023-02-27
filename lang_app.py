import warnings
import streamlit as st
import spacy
import pandas as pd

from vocab_extract import VocabExtractor
from vocab_extract import get_meaning_and_example_sentence
TOKEN_STATUS_THRESHOLD = 8
st.set_page_config(layout="wide")

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

query = st.text_area("Enter Text Here!", 
"""Ich habe heute Morgen lange überlegt, ob ich mich für den neuen Kurs anmelden soll oder nicht.
Letztendlich habe ich mich entschieden, mich anzumelden, weil ich meine Deutschkenntnisse verbessern möchte.
""",
)

if query != "":
    doc = nlp(query)
    extractions = []
    for sentence in doc.sents:
        extractions.extend(vocab_ext.extract_vocab(sentence))


    df_temp = pd.DataFrame({"WORDS": extractions})
    df_temp.drop_duplicates(inplace=True)
    

    df_temp["WORD STATUS"] = df_temp["WORDS"].apply(
        lambda x: vocab_ext.check_token_status(x, token_status_threhold=TOKEN_STATUS_THRESHOLD) 
    )
  

    easy_words_list = df_temp[df_temp["WORD STATUS"] == "easy"]["WORDS"].tolist()
    
    
    if easy_words_list:
        easy_words_list = ",".join( easy_words_list)
        warnings.warn(f"The words are considred easy and are being ignored = {easy_words_list}. Increase token_status_threhold to 8 to include all words")
    df_temp = df_temp[df_temp["WORD STATUS"] == "hard"]
    

    df_temp["ARTIFACT"] = df_temp["WORDS"].apply(
        lambda x: get_meaning_and_example_sentence(x) 
    )
    df = pd.DataFrame(
        df_temp["ARTIFACT"].tolist(),
        index=df_temp.index,
        columns=["Meaning", "Example DE", "Example EN"],
    )
    df.insert(loc=0, column="WORDS", value=df_temp["WORDS"])

    st.dataframe(df, use_container_width=True)

    csv = convert_df(df)

    st.download_button(
        "Press to Download", csv, "file.csv", "text/csv", key="download-csv"
    )
