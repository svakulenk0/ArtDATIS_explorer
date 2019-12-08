#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on Dec 8, 2019
.. codeauthor: svitlana vakulenko
    <svitlana.vakulenko@gmail.com>

Index docs into ES
https://qbox.io/blog/building-an-elasticsearch-index-with-python
'''
from settings import *
import glob

txts_path = '%s/artdatis/tagging/OCRed/typed/' % DATA_PATH
text_corpus = []
bulk_data = [] 
# filter out and collect text files
for file_path in glob.glob(txts_path+'*_text.txt'):
    with open(file_path) as file:
        text = file.read()
        # filter duplicates
        if text not in text_corpus:
            text_corpus.append(text)
            with open(file_path.split('_text.txt')[0]+'_path.txt') as path_file:
                path = path_file.read().strip()
                # create the _source data for the Elasticsearch doc
                data_dict = {
                    "file_path": path,
                    "text": text
                }
               
                bulk_data.append({"_index": INDEX_NAME, "_type": TYPE_NAME, "_source": data_dict})
print("Loaded %d documents"%len(text_corpus))


from elasticsearch import Elasticsearch
# create ES client, create index
es = Elasticsearch(hosts = [ES_HOST])
if es.indices.exists(INDEX_NAME):
    print("deleting '%s' index..." % (INDEX_NAME))
    res = es.indices.delete(index = INDEX_NAME)
    print(" response: '%s'" % (res))

request_body = {
    "settings" : {
        "number_of_shards": 1,
        "number_of_replicas": 0
    }
}
print("creating '%s' index..." % (INDEX_NAME))
res = es.indices.create(index = INDEX_NAME, body = request_body)
print(" response: '%s'" % (res))

# bulk index the data
print("bulk indexing...")
res = es.bulk(index = INDEX_NAME, body = bulk_data, refresh = True)

# sanity check
res = es.search(index = INDEX_NAME, size=2, body={"query": {"match_all": {}}})
print("results:")
for hit in res['hits']['hits']:
    print(hit["_source"])
