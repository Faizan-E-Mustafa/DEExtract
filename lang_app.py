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

from inverted_index import InvertedIndex

inv_index = InvertedIndex()


@st.cache_data
def load_inverted_index(filepath):
    inverted_index = inv_index.load_inverted_index(filepath)
    return inverted_index


@st.cache_data
def load_topic_dataset(filepath):
    dataset_topic = inv_index.load_dataset(filepath)
    return dataset_topic


@st.cache_data
def convert_df(df):
    return df.to_csv(index=False).encode("utf-8")


@st.cache_data
def load_model():
    tokenizer = AutoTokenizer.from_pretrained(
        "C:/Users/femustafa/Desktop/Language_app/t5-base"
    )
    model = AutoModelForSeq2SeqLM.from_pretrained(
        "C:/Users/femustafa/Desktop/Language_app/t5-base"
    )
    return model, tokenizer


st.write(
    """
## German Vocabulary Extractor
"""
)

with st.sidebar:
    st.write(
        """
    ### Vocab Extractor
    """
    )
    TOKEN_STATUS_THRESHOLD = st.slider(
        label="Frequency Threshold",
        min_value=3.,
        max_value=6.,
        # step = 0.2,
        key=1,
        value=5.,
        help="Words having frequecy greater than the threshold will be ignored because they are easy and frequent. Set max threshold to include all possible words. ",
    )

    st.write(
        """
    ### Synthetic Text Retriever
    """
    )
    LANG_LEVEL = st.selectbox("Readability Level", ("Intermediate", "Advanced"))
    LANG_LEVEL = LANG_LEVEL.lower()

    topic_selected = st.selectbox("Select Topic", ("Politik", "Wirtschaft"))

    # st.write(
    #     """
    # ### T5 Model parameters
    # """
    # )

    # TEMPERATURE = st.slider(
    #     label="Temperature", min_value=0.0, max_value=1.0, key=2, value=1.0
    # )

    # TOPK = st.slider(label="Top K", min_value=0, max_value=10, key=3, value=3)

# Die Branche hat sich in den letzten Jahren rapide entwickelt.
with st.form(key="my_form"):
    query = st.text_area(
        "Enter Text Here!",
        """Ich werde heute ein neues Auto kaufen.
Ich fahre mit dem Zug nach Islamabad.
Der Zug fährt pünktlich um vier Uhr ab.
Paare lernen gewöhnlich ihre Unterschiede anzunehmen. 
Ich habe ein schönes Restaurant entdeckt.
Das Hotel befindet sich an einem kleinen See.
Ich muss mich anstrengen, um die gesamte Arbeit rechtzeitig zu erledigen.
""",
height = 140
    )
    submit_button = st.form_submit_button(label="Submit")

# import pdb; pdb.set_trace()
if submit_button and query:
    placeholder = st.empty()

    with placeholder.container():
        st.write("Processing .........")

    doc = nlp(query)
    extractions = []
    for sentence in doc.sents:
        extractions.extend(vocab_ext.extract_vocab(sentence))

    df_temp = pd.DataFrame({"WORDS": extractions})
    df_temp.drop_duplicates(inplace=True)

    df_temp["WORD STATUS"] = df_temp["WORDS"].apply(
        lambda x: vocab_ext.check_token_status(
            x, token_status_threhold=TOKEN_STATUS_THRESHOLD
        )
    )

    easy_words_list = df_temp[df_temp["WORD STATUS"] == "easy"]["WORDS"].tolist()

    if easy_words_list:
        easy_words_list = ",".join(easy_words_list)
        warnings.warn(
            f"The words are considred easy and are being ignored = {easy_words_list}. Increase token_status_threhold to 8 to include all words"
        )
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

    placeholder.empty()

    st.dataframe(df, use_container_width=True)

    csv = convert_df(df)

    st.download_button(
        "Press to Download", csv, "file.csv", "text/csv", key="download-csv"
    )

st.write(
    """
## Synthetic Text Retriever
"""
)

col1, col2 = st.columns((2, 2))

with col1:
    with st.form(key="vocab_form"):
        vocab_list = st.text_area(
            "Enter Verbs Here!",
            """kommen\nbeginnen\nverdienen\nbekommen
    """,
        )
        vocab_submit_button = st.form_submit_button(label="Submit")


import config


if vocab_submit_button and vocab_list:
    vocab_list = [i.lower().strip() for i in vocab_list.split("\n")]

    inverted_index = load_inverted_index(
        config.DATA_ROOT / f"inverted_index_{topic_selected}_{'b1' if LANG_LEVEL=='intermediate' else 'c1'}.json"
    )

    doc_importance = inv_index.index_lookup(
        exracted_vocab=vocab_list, inverted_index=inverted_index, topn_docs=3
    )

    dataset_topic = load_topic_dataset(
        config.DATA_ROOT / f"dataset_{topic_selected}_{'b1' if LANG_LEVEL=='intermediate' else 'c1'}.json"
    )

    for doc_id, score in doc_importance:
        text_vocab = dataset_topic[doc_id - 1]["vocab"]
        common_vocab = set([i for i in text_vocab if i in vocab_list])

        st.write(dataset_topic[doc_id - 1]["text"])
        with st.expander("See explanation"):
            st.write(f"Text Vocabulary = {text_vocab}")
            st.write(f"Common Vocabulary = {common_vocab}")

    # common_vocab_store = []
    # max_samples = 3
    # generate_count = 0
    # skipped = []
    # for doc_id, score in doc_importance:
    #     if generate_count == max_samples:
    #         break
    #     # print(dataset_topic[doc_id-1])
    #     text_vocab = dataset_topic[doc_id-1]["vocab"]
    #     common_vocab = set([i for i in text_vocab if i in vocab_list])
    #     # import pdb; pdb.set_trace()
    #     if common_vocab in common_vocab_store:
    #         skipped.append([dataset_topic[doc_id-1]["text"], common_vocab])
    #         continue

    #     else:
    #         generate_count = generate_count + 1
    #         common_vocab_store.append(common_vocab)

    #         st.write(dataset_topic[doc_id-1]["text"])
    #         st.write(f"Common Vocab = {common_vocab}")


from transformers import AutoModelForSeq2SeqLM
from transformers import AutoTokenizer


def gen(sample, top_k, temperature=1):
    input_ids = tokenizer(sample, return_tensors="pt").input_ids
    outputs = model.generate(
        input_ids.to(device="cpu"),
        max_new_tokens=200,
        do_sample=True,
        #    top_p=0.92,
        top_k=top_k,
        no_repeat_ngram_size=3,
        temperature=temperature,
        # num_beams=1,
        # num_return_sequences=3,
    )
    return tokenizer.decode(outputs[0], skip_special_tokens=True)


# if vocab_submit_button and vocab_list:
#     st.write(
#         """
#     ### T5 Generated Text 
#     """
#     )
#     # vocab_list = [i.lower().strip() for i in vocab_list.split("\n")]
#     model, tokenizer = load_model()

#     unique_vocab_str = " ".join(
#         [f"{e} <extra_id_{i+1}>" for i, e in enumerate(vocab_list)]
#     )
#     document = topic_selected + " <extra_id_0> " + unique_vocab_str

#     result = gen(document, top_k=TOPK, temperature=TEMPERATURE)
#     st.write(result)
