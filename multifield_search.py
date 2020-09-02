from bert_serving.client import BertClient
from elasticsearch import Elasticsearch
from datetime import datetime
import os
import numpy as np


def connect_es():
    es = Elasticsearch(HOST = 'https://localhost', PORT = 9200)
    return es

def printDB(name):
    count = 1
    while True:
        try:
            temp = es.get(index = name, id = count)
            print(temp['_source'])
            print(' ')
            count+=1
        except Exception as e:
            break





def getSimilarVectors(index, number, sentence_index,sentences_list_2, q_embedding_vectors):
    #number represents the size of search result
    vector = q_embedding_vectors[sentence_index]
    query_doc = {
      "size" : number,
      "query": {
          "function_score":{
                "query":{
                    "match_all":{
                        }
                    },
                "functions":[
                    {
                        "filter": {"match": {"student_type": "ambitious"}},
                        "weight": 1.0

                    },
                    {
    
                        "filter": {"range": {"age": {"gte": "22"}}},
                        "weight": 6.0

                    },
                    {
                        "script_score": {
                            "script": {
                                "source": "cosineSimilarity(params.query_vector, 'sent_vec') + 0.5",
                                "params": {
                                    "query_vector": vector,
                                }
                            }
                        }
                    }
                ]

            }
        }
    }
    sentences = []
    search_result = es.search(index = index, body = query_doc)
    for i in range(len(search_result['hits']['hits'])):
	      x = search_result['hits']['hits'][i]['_source']
	      sentences.append(x['objective'])
    return search_result, sentences



def bert_embeddings(input_data, query):
    bc = BertClient()
    input_embeddings = bc.encode(input_data)
    query_embeddings = bc.encode(query)
    return input_embeddings, query_embeddings
    pass


def prepare_template_for_insertion(age, name, sentences_list, sentences_list_2, embedding_vectors,list_index):
    #entry = datetime.now()
    objective = sentences_list[list_index]
    new_sent_2 = sentences_list_2[list_index]
    sent_vec = embedding_vectors[list_index].tolist()
    #sent_vec_2 = sent_2_embeddings[list_index].tolist()
    return {'age': age, 'student_type':new_sent_2, 'name': name, 'objective':objective, 'sent_vec':sent_vec, }
    pass

def insert_document(json_file, index_name, index_in_sentence_list):
    es.index(index = index_name, id = index_in_sentence_list + 1, body = json_file)

if __name__ == '__main__':
    es = connect_es()
    index_name = "student_multi"
    sentences_list = [
        # phone related
        'I want to score good grades in my exams',
        'Good grades can help me in getting a good job',
        'I dont like these classes',
        'Math class is boring',
        'I like to play chess and I like to code',
        'we dont get to play often and I hate my science teacher.'
    ]
    
    sentences_list_2 = [
        # phone related
        'sincere',
        'ambitious',
        'dull',
        'moody',
        'intelligent',
        'dull'
    ]
    query_list = [
        # phone related
        'I wish best result in the test',
        'better academics will assist me in brighter career',
        'I have a lot of aversion to  these lectures',
        'classes with mathematics numbers are so lame',
        'I have always loved strategic games and computers',
        'I hate anything related to science'
    ]

    embedding_vectors, q_embedding_vectors =  bert_embeddings(sentences_list, query_list)
    
    
    ############################################ INSERTION######################################
    """
    #student_name_age = [['student_name(string)', age(int)]]
    student_name_age = [['First', 18], ['Second', 19], ['Third', 20], ['Fourth', 21], ['Fifth', 22], ['Sixth', 23]]
    for i in range(len(student_name_age)):
        #prepare_template_for_insertion(age, name, sentences_list, sentences_list_2, embedding_vectors,list_index):
        template_for_entry = prepare_template_for_insertion(student_name_age[i][1], student_name_age[i][0], sentences_list, sentences_list_2, embedding_vectors, i)
        insert_document(template_for_entry, index_name, i)
    """

    
    ##############################################SEARCH######################################
    """

    top_n_results = 2
    
    for i in range(len(query_list)):
        #print(getSimilarVectors(index_name, top_n_results, i, q_embedding_vectors))
        search_result, top_sentences = getSimilarVectors(index_name, top_n_results, i, sentences_list_2, q_embedding_vectors)
        print(query_list[i], end = '; ')
        print(top_sentences)
        print(' ')
    """

