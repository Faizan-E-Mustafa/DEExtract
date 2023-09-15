from vocab_extract import VocabExtractor
import spacy
import json
from tqdm import tqdm

from datasets import load_dataset, load_metric

vocab_ext = VocabExtractor()
nlp = spacy.load("de_core_news_sm")


# raw_datasets = load_dataset("gnad10")
# # import pdb; pdb.set_trace()
# ClassLabels = raw_datasets['train'].features["label"]
# for ds_name, ds in raw_datasets.items():
#     print(ds_name)

#     texts = ds["text"]
#     labels = ds["label"]
#     label_names = ClassLabels.int2str(labels)
#     with open(f"{ds_name}.json" , "w", encoding="utf-8") as f:
#         for text, label_name in tqdm(zip(texts, label_names), total=len(texts)):
#             # if "Der Volltext dieses auf Agenturmeldungen basierenden Artikels steht aus rechtlichen Gründen nicht mehr zur Verfügung." in text:
#             text = text.replace("Der Volltext dieses auf Agenturmeldungen basierenden Artikels steht aus rechtlichen Gründen nicht mehr zur Verfügung.", "")
#             doc = nlp(text)
#             # sentences = doc.sents
#             sections = [text]
#             if len(list(doc.sents)) > 3:

#                 sections = []
#                 section = []
#                 for i, sent in enumerate(doc.sents):
#                     # print(sent.text)


#                     if i !=0 and i % 3 == 0:
#                         sections.append(" ".join(section))
#                         # import pdb; pdb.set_trace()
#                         section = []

#                     section.append(sent.text)

#                 if section:
#                     sections.append(" ".join(section))


#             for section in sections:
#                 sec = nlp(section)
#                 extracted_vocab = []
#                 for sentence in sec.sents:
#                     extracted_vocab.extend(vocab_ext.extract_vocab(sentence))

#                 unique_vocab = []
#                 for i in extracted_vocab:
#                     if i not in unique_vocab:
#                         unique_vocab.append(i)

#                 # token_status_threhold = 4.5
#                 # # import pdb; pdb.set_trace()
#                 # unique_vocab = [i for i in unique_vocab if vocab_ext.check_token_status(i, token_status_threhold) == "easy"]

#                 # if len(unique_vocab) < 3  or len(unique_vocab) > 5:
#                 #     continue


#                 unique_vocab = " " .join([f'{e} <extra_id_{i}>' for i, e in enumerate(unique_vocab)])

#                  # document = entry["topic"] + " </s> " +  unique_vocab + " </s>"

#                 # document = label_name + " <extra_id_0> " +  unique_vocab
#                 document = unique_vocab

#                 if unique_vocab:
#                     json.dump({"document": document, "summary": section}, f)
#                     f.write('\n')


############################################


# raw_datasets = load_dataset("mlsum", 'de')
# # ClassLabels = raw_datasets['train'].features["label"]
# for ds_name, ds in raw_datasets.items():
#     print(ds_name)

#     texts = ds["text"]
#     labels = ds["topic"]

#     # label_names = ClassLabels.int2str(labels)
#     with open(f"filtered_topics_{ds_name}.json" , "w", encoding="utf-8") as f:
#         for text, label_name in tqdm(zip(texts, labels), total=len(texts)):
#             # {'bildung', 'reisefuehrer', 'reise',  'wirtschaft', 'politik', 'geld',  'sport', 'digital', 'stil',  'kultur', 'karriere', 'auto'}
#             if label_name not in { 'politik', 'wirtschaft'}:
#                 continue
#             if len(text.split())>200:
#                 continue
#             doc = nlp(text)
#             sections = [text]

#             if len(list(doc.sents)) > 4:

#                 sections = []
#                 section = []
#                 for i, sent in enumerate(doc.sents):


#                     if i !=0 and i % 4 == 0:
#                         sections.append(" ".join(section))
#                         # import pdb; pdb.set_trace()
#                         section = []

#                     section.append(sent.text)

#                 if section:
#                     sections.append(" ".join(section))

#             for section in sections:
#                 sec = nlp(section)
#                 extracted_vocab = []
#                 for sentence in sec.sents:
#                     extracted_vocab.extend(vocab_ext.extract_vocab(sentence))

#                 unique_vocab = []
#                 for i in extracted_vocab:
#                     if i not in unique_vocab:
#                         unique_vocab.append(i)

#                 token_status_threhold = 4.5
#                 # import pdb; pdb.set_trace()
#                 unique_vocab = [i for i in unique_vocab if vocab_ext.check_token_status(i, token_status_threhold) == "easy"]

#                 if len(unique_vocab) < 3  or len(unique_vocab) > 5:
#                     continue

#                 # unique_vocab = " </s> ".join(unique_vocab)
#                 # # document = label_name + " <extra_id_0> " +  unique_vocab + " <extra_id_1>"
#                 # document = label_name + " </s> " +  unique_vocab + " </s>"


#                 # json.dump({"document": document, "summary": text}, f)
#                 # f.write('\n')


#                 json.dump({"topic": label_name, "unique_vocab": unique_vocab, "section": section }, f)
#                 f.write('\n')

############################################


###########################################
import config

data = []
with open(config.DATA_ROOT / "gpt_dataset_c2.json", "r") as f:
    for line in f:
        data.append(json.loads(line))


with open(config.DATA_ROOT / "train.json", "w", encoding="utf-8") as f:
    for entry in data:
        unique_vocab = entry["vocab"]

        unique_vocab_str = " ".join(
            [f"{e} <extra_id_{i+1}>" for i, e in enumerate(entry["vocab"])]
        )

        document = (
            entry["topic"] + " <extra_id_0> " + unique_vocab_str
        )  # + f" {original_text} <extra_id_{len(unique_vocab)+1}>"

        json.dump({"document": document, "summary": entry["text"]}, f)
        f.write("\n")
