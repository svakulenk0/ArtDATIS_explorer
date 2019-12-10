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
import re

# n first characters for the doc preview
LIMIT_START = 100

txts_path = '%s/artdatis/tagging/OCRed/typed/' % DATA_PATH
text_corpus = []

def corpus_iterator():
    # filter out and collect text files
    for file_path in glob.glob(txts_path+'*_text.txt'):
        with open(file_path, encoding="utf-8") as file:
            text = file.read()
            # filter duplicates
            if text not in text_corpus:
                text_corpus.append(text)
                text = re.sub(' +', ' ', text)
                start_text = text.lstrip()[:LIMIT_START]
                with open(file_path.split('_text.txt')[0]+'_path.txt') as path_file:
                    path = path_file.read().strip()
                    yield {
                            "_index": INDEX_NAME,
                            "_type": TYPE_NAME,
                            "_source": {"file_path": path, "text": text, "start_text": start_text},
                        }
    print("Loaded %d documents"%len(text_corpus))


from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

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
bulk(es, corpus_iterator())

# sanity check
res = es.search(index = INDEX_NAME, size=2, body={"query": {"match_all": {}}})
print("results:")
for hit in res['hits']['hits']:
    print(hit["_source"])
