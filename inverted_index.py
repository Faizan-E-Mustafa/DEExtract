import json
from collections import defaultdict, Counter
from tqdm import tqdm 

import config

# def filter_gpt_dataset():
#     raw_data = []
#     with open("gpt_dataset.json", "r", encoding = "utf-8") as f:
#         for i in f:
#             raw_data.append(json.loads(i))

#     with open("gpt_dataset_filtered.json", "w", encoding = "utf-8") as f:
#         for i, entry in enumerate(raw_data):

#             json.dump({"id": i+1,  "text": entry["text"], "vocab": entry["vocab"]}, f)
#             f.write("\n")


from vocab_extract import VocabExtractor
import spacy

class InvertedIndex:
    def __init__(
        self,
    ) -> None:
        pass

    def load_dataset(self, gpt_dataset_path):
        raw_data = []
        with open(gpt_dataset_path, "r", encoding="utf-8") as f:
            for i in f:
                raw_data.append(json.loads(i))
        return raw_data

    def create_inverted_index_for_topic(self, dataset, topic, level):
        topic_dataset = self.filter_by_topic(dataset, topic)

        nlp = spacy.load("de_core_news_sm")
        
        vocab_ext = VocabExtractor()

        index_posting_list = defaultdict(list)

        for entry in tqdm(topic_dataset):

            # override the vocab that was used to generate the samples
            doc = nlp(entry["text"])
            extracted_vocab = [] 
            for sentence in doc.sents:
                extracted_vocab.extend(vocab_ext.extract_vocab(sentence))
            unique_vocab = []
            for i in extracted_vocab:
                if i not in unique_vocab:
                    unique_vocab.append(i)
            entry["vocab"] = unique_vocab

            # vocab = entry["vocab"]
            vocab = unique_vocab
            sample_id = entry["id"]

            for token in vocab:
                index_posting_list[token].append(sample_id)

        with open(
            config.DATA_ROOT / f"inverted_index_{topic}_{level}.json", "w", encoding="utf-8"
        ) as f:
            json.dump(
                index_posting_list,
                f,
            )

        with open(
            config.DATA_ROOT / f"dataset_{topic}_{level}.json", "w", encoding="utf-8"
        ) as f:
            for i in topic_dataset:
                json.dump(i, f)
                f.write("\n")


    def filter_by_topic(self, gpt_dataset, topic):
        topic_dataset = []
        i = 1
        for entry in gpt_dataset:
            if entry["topic"] == topic:
                vocab = [v.lower() for v in entry["vocab"]]

                topic_dataset.append(
                    {
                        "id": i,
                        "text": entry["text"],
                        "vocab": vocab,
                        "topic": entry["topic"],
                    }
                )
                i = i + 1

        return topic_dataset

    def load_inverted_index(self, filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            inverted_index = json.load(f)
        return inverted_index

    def index_lookup(self, exracted_vocab, inverted_index, topn_docs):

        posting_lists = [v for token in exracted_vocab for v in inverted_index.get(token, [])]
        doc_importance = Counter(posting_lists).most_common(topn_docs)
        print(doc_importance)
        
        return doc_importance



if __name__ == "__main__":
    lang_level = "c2"

    inv_index = InvertedIndex()
    complete_dataset = inv_index.load_dataset(
        gpt_dataset_path=config.DATA_ROOT / f"gpt_dataset_{lang_level}.json"
    )
    inv_index.create_inverted_index_for_topic(complete_dataset, topic="wirtschaft", level=lang_level)
    inv_index.create_inverted_index_for_topic(complete_dataset, topic="politik", level=lang_level)

    inverted_index = inv_index.load_inverted_index(
        config.DATA_ROOT / f"inverted_index_politik_{lang_level}.json"
    )
    doc_importance = inv_index.index_lookup(exracted_vocab=[ "finden", "unternehmen"], inverted_index=inverted_index, topn_docs= 3)

    dataset_politik = inv_index.load_dataset(config.DATA_ROOT / f"dataset_politik_{lang_level}.json")

    for doc_id, score in doc_importance:
        print(dataset_politik[doc_id-1])