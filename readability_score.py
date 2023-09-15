import json
import config
import textstat

lang_level = "b1"

raw_data = []
with open(config.DATA_ROOT / f"gpt_dataset_{lang_level}.json", "r", encoding="utf-8") as f:
    for i in f:
        raw_data.append(json.loads(i))

lang_level = "c2"
raw_data_c2 = []
with open(config.DATA_ROOT / f"gpt_dataset_{lang_level}.json", "r", encoding="utf-8") as f:
    for i in f:
        raw_data_c2.append(json.loads(i))

lang_level = "b1"
raw_data_b1 = []
with open(config.DATA_ROOT / f"gpt_dataset_{lang_level}.json", "r", encoding="utf-8") as f:
    for i in f:
        raw_data_b1.append(json.loads(i))



b1_scores = []
c2_scores = []
for b1, c2 in zip(raw_data_b1, raw_data_c2):
    b1 = b1["text"]
    c2 = c2["text"]
    # print(textstat.flesch_reading_ease(b1 ))
    # print(textstat.wiener_sachtextformel(b1, 1))

    # print(textstat.flesch_reading_ease(c2 ))
    # print(textstat.wiener_sachtextformel(c2, 1))
    b1_scores.append(textstat.wiener_sachtextformel(b1, 2))
    c2_scores.append(textstat.wiener_sachtextformel(c2, 2))


import statistics
print(statistics.mean(b1_scores) )
print(statistics.mean(c2_scores) )
