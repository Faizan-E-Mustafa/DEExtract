from datasets import load_dataset, load_metric
import config

from transformers import AutoModelForSeq2SeqLM
from transformers import AutoTokenizer

data_dir = str(config.DATA_ROOT) 
data_files = {"train": "train.json", "test": "test.json"}
raw_datasets = load_dataset(
            
            data_dir, data_files=data_files,
        )
    
tokenizer = AutoTokenizer.from_pretrained("C:/Users/femustafa/Desktop/Language_app/t5-base")
model = AutoModelForSeq2SeqLM.from_pretrained("C:/Users/femustafa/Desktop/Language_app/t5-base")

def gen(sample, top_k):

    input_ids = tokenizer(sample, return_tensors="pt").input_ids
    outputs = model.generate(input_ids.to(device='cpu'), 
    max_new_tokens= 200,
    do_sample=True,
#    top_p=0.92, 
    top_k=top_k,
    no_repeat_ngram_size = 3,
    # temperature=0.2,
    # num_beams=1,
    # num_return_sequences=3,
      )
    print(tokenizer.decode(outputs[0], skip_special_tokens=True))

def temp(i, top_k):
    print(raw_datasets["test"]["document"][i])
    gen(raw_datasets["test"]["document"][i], top_k)

for i in range(5):
    print("top 0")
    temp(i, top_k=3)
    print("top 5")
    temp(i, top_k=30)
    print("===========================")
