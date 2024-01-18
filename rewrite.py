import openai
import json

from variable import *

openai.api_key = APIKEY
DATA="VGCOCO_sents.json"
MAXCAPTIONS=300


def get_completion(prompt, model="gpt-3.5-turbo-16k"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]

with open(DATA, "r") as f:
    input_data = json.load(f)
# batch = int(len(input_data)/75)
# for i in range(batch+1):
#     if i == batch:
#         input_data_300 = input_data[i*75:]
#     elif i<1975:
#         continue
#     elif i > 600*4:
#         break
#     else:
#         input_data_300 = input_data[i*75:(i+1)*75]
#     prompt = f"""Rewrite the sentences in the square bracket.
    
#     sentences: {input_data_300}

#     provide them in JSON format where keys are the sentences and values are the rewritten sentences.
#     """
#     print(f"running for {i+1}")
#     response_16K = get_completion(prompt)
#     response_16K = response_16K.replace(",\n}", "\n}")
#     jaon_16k = json.loads(response_16K)
#     with open(f'output_75_{i+1}.json', 'w') as f:
#         json.dump(jaon_16k, f)
batch = int(len(input_data)/MAXCAPTIONS)
for i in range(batch+1):
    if i == batch:
        input_data_300 = input_data[i*MAXCAPTIONS:]
    elif i<915:
        continue
    elif i > 1000:
        break
    else:
        input_data_300 = input_data[i*MAXCAPTIONS:(i+1)*MAXCAPTIONS]
    try:
        prompt = f"""Rewrite the sentences in the square bracket.
        
        sentences: {input_data_300}

        provide them in JSON format where keys are the sentences and values are the rewritten sentences.
        """
        print(f"running for {i+1}")
        response_16K = get_completion(prompt)
        response_16K = response_16K.replace(",\n}", "\n}")
        jaon_16k = json.loads(response_16K)
    except Exception as e:
        print(f"Ignored iteration {i+1} due to an error: {e}")
        continue
    with open(f'output_300_{i+1}.json', 'w') as f:
        json.dump(jaon_16k, f)