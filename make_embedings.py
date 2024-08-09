import os
import json
import requests
import multiprocessing 
from sentence_transformers import SentenceTransformer

from datetime import datetime

multiprocessing.set_start_method('spawn')


os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1' 


startTime = datetime.now()

model = SentenceTransformer('all-mpnet-base-V2',force_download = True)

r = requests.get('https://raw.githubusercontent.com/DataTalksClub/llm-zoomcamp/main/01-intro/documents.json')

open('documents.json', 'wb').write(r.content)

with open('documents.json', 'rt') as f_in:
    docs_raw = json.load(f_in)

documents = []

for course_dict in docs_raw:
    for doc in course_dict['documents']:
        doc['course'] = course_dict['course']
        documents.append(doc)

cpus = multiprocessing.cpu_count() - 1

def make_vecs(doc):
    doc['vector_text'] = model.encode(doc['text']).tolist()
    return doc

if __name__=='__main__':
    
    with multiprocessing.Pool(cpus) as pool:
        documents = pool.map(make_vecs, documents)

    with open('documents_with_vectors.json','wt') as outfile:
        json.dump(documents, outfile, indent=4)

print(datetime.now() - startTime)