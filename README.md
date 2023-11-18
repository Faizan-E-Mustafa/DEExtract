# DEExtract
Extract german vocabulary from text and use list of verbs to generate sample texts on specific topic at a particular language proficiency level.

#### Verb Extraction:
![website demo](dump/images/vocab_extraction_demo.PNG)

#### Synthetic Text Retriver:
![website demo](dump/images/retriever_demo.PNG)

# Package Installation

```bash
pip install -r requirements.txt
```

## Data Preparation:
Note: The data is already uploaded in the repository. Skip to [next](#Dashboard) section to start the dashboard

`dataset_prep.py`: Filter data from MLSUM dataset using topic names and use `VocabExtractor` to extract vocabulary. Further details are mentioned in 3.1 of the paper. The output is stored in `data/filtered_topics_{dataset_split_name}.json`

`chatgpt.py`: Generated synthetic using the extracted vocab from `data/filtered_topics_train.json` and store the result as `data/gpt_dataset_{cefr_level}.json`

`ìnverted_index.py`: Split the `data/gpt_dataset_{cefr_level}.json` by topic also `dataset_{topic}_{cefr_level}.json` and create inverted index `inverted_index{topic}_{cefr_level}.json`

## Dashboard
`lang_app.py`: Start the dashboard using the following command

```bash
streamlit run lang_app.py 
```

### Utils: 

`readability_score.py`: Calculate readability scores

## Text Generation Using T5

Note: This section is not part of the publication.

Use the vocabulary and topic to create a sythetic paragraph. The model was develeped as an alternative for the ChatGPT. However, the model sometimes does not generate coherent text.

`dataset_prep.py`: Prepare the dataset.

`train.py`: Train the T5 model

`predict.py`: Generate the text using some input topic and list of vocabulary. 

![website demo](dump/images/t5_demo.PNG)

### Dataset Terms and Conditions:

Processed dataset is also avaliable as [HuggingFace Dataset](https://huggingface.co/datasets/femustafa/DEExtract). 

Dataset is created using ChatGPT and further use is permitted as long the use comply with the [Terms and Conditions](https://openai.com/policies/terms-of-use) of OpenAI.

### Cite

To be updated






