import streamlit as st
import spacy
import pandas as pd

from vocab_extract import VocabExtractor
from vocab_extract import get_meaning_and_example_sentence

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

query = st.text_input("Enter Text!", "")

if query != "":
    doc = nlp(query)
    extractions = []
    for sentence in doc.sents:
        extractions.extend(vocab_ext.extract_verbs(sentence))
    df_temp = pd.DataFrame({"VERBS": extractions})
    # import pdb; pdb.set_trace()

    df_temp["ARTIFACT"] = df_temp["VERBS"].apply(
        lambda x: get_meaning_and_example_sentence(x)
    )
    df = pd.DataFrame(
        df_temp["ARTIFACT"].tolist(),
        index=df_temp.index,
        columns=["Meaning", "Example DE", "Example EN"],
    )
    df.insert(loc=0, column="VERBS", value=df_temp["VERBS"])

    st.dataframe(df, use_container_width=True)

    csv = convert_df(df)

    st.download_button(
        "Press to Download", csv, "file.csv", "text/csv", key="download-csv"
    )
