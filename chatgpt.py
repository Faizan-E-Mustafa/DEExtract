import json 
import os
import openai

import logging
import time
import config

logging.basicConfig(
    filename="gpt_logs",
    filemode="a",
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
    level=logging.DEBUG,
)

def syntheize_samples():
    
        data = []
        with open(config.DATA_ROOT / "filtered_topics_train.json","r") as f:
            for line in f:
                data.append(json.loads(line))

        # data = data[5952:]
        # import pdb; pdb.set_trace()
        
        openai.api_key = os.getenv("OPENAI_API_KEY")
        samples_created = 0
        i = 0

        with open("gpt_dataset.json", "w", encoding="utf-8") as myfile:
            for i in range(20000):
                try:

                    completion = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[
                           
                            #  {
                            #     "role": "user",
                            #     "content": f'Act like a synthetic data generator that knows German at B1 CEFR level. Write a short paragraph on the topic of "{data[i]["topic"]}" that should use verbs mentioned in this list: {data[i]["unique_vocab"]}. The grammatical structure and vocabulary should not be complex.',
                            # },
                            {
                                "role": "user",
                                "content": f'Act like a synthetic data generator that knows German at C2 CEFR level. Write a short paragraph on the topic of "{data[i]["topic"]}" that should use verbs mentioned in this list: {data[i]["unique_vocab"]}. The grammatical structure and vocabulary should be complex. Do not mention that the paragraph is synthetically generated.',
                            },
                           
                           
                        ],
                    )
                    # import pdb; pdb.set_trace()
                    text = completion.choices[0].message["content"]



                    if text:
                        
                        json.dump({"text": text, "topic": data[i]["topic"], "vocab": data[i]["unique_vocab"]}, myfile)
                        myfile.write('\n')
                        # myfile.write(text + "\n")
                        samples_created = samples_created + 1
                        i = i + 1
                    # import pdb; pdb.set_trace()
                    logging.info(text)
                    
                    logging.info(f"Sample created until now = {samples_created}")

                    # time.sleep(1)

                except Exception as e:
                    logging.error(f"Attempt Failed for iteration = {i}")
                    logging.error(e)
                    time.sleep(10)


syntheize_samples()