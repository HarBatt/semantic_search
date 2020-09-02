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

#in general a scalar is required for consinesim to avoid negative values, say +1.0

def getSimilarVectors(index, number, sentence_index,q_embedding_vectors):
    #number represents the size of search result
    vector = q_embedding_vectors[sentence_index]
    query_doc = {
      "size" : number,
      "query": {
        "script_score": {
          "query" : {
            "match_all" : {}
          },
          "script": {
              
            "source": "cosineSimilarity(params.query_vector, 'sent_vec') + 0.5",
            "params": {
              "query_vector": vector
            }
          }
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


def get_embeddings():
    path_to_embeddings = 'D:/Elasticsearch/code/text.txt'
    path_to_query_embeddings = 'D:/Elasticsearch/code/query.txt'

    f1 = open(path_to_embeddings, 'r+')
    lines_1 = [line1 for line1 in f1.readlines()]
    f1.close()
    embeddings = get_embeddings_helper(lines_1)

    f = open(path_to_query_embeddings, 'r+')
    lines = [line for line in f.readlines()]
    f.close()
    query_embeddings = get_embeddings_helper_QUERY(lines)
    return embeddings, query_embeddings
    pass


def get_embeddings_helper(matrix):
    final_matrix = []
    count = 0
    n = 6
    emb_len = 512
    #n -> number of documents in the index
    #emb_len -> length of embeddings.
    for i in range(n):
        temp_matrix = []
        for j in range(emb_len):
            embedding_ele = matrix[count]
            new_embedding_ele = float(embedding_ele[:len(embedding_ele)-2])
            temp_matrix.append(new_embedding_ele)
            count+=1
            
        final_matrix.append(temp_matrix)
    return final_matrix

def get_embeddings_helper_QUERY(matrix):
    final_matrix = []
    count = 0
    n = 6
    emb_len = 512
    #n -> number of documents in the index
    #emb_len -> length of q-embeddings.
    for i in range(n):
        temp_matrix = []
        for j in range(emb_len):
            embedding_ele = matrix[count]
            new_embedding_ele = float(embedding_ele[:len(embedding_ele)-2])
            temp_matrix.append(new_embedding_ele)
            count+=1
            
        final_matrix.append(temp_matrix)
    return final_matrix


def prepare_template_for_insertion(age, name, sentences_list, embedding_vectors, list_index):
    entry = datetime.now()
    objective = sentences_list[list_index]
    sent_vec = embedding_vectors[list_index].tolist()
    return {'age': age, 'entry':entry, 'name': name, 'objective':objective, 'sent_vec':sent_vec}
    pass

def insert_document(json_file, index_name, index_in_sentence_list):
    es.index(index = index_name, id = index_in_sentence_list + 1, body = json_file)

if __name__ == '__main__':
    es = connect_es()
    index_name = "student_bert"
    sentences_list = [
        # phone related
        'I want to score good grades in my exams',
        'Good grades can help me in getting a good job',
        'I dont like these classes',
        'Math class is boring',
        'I like to play chess and I like to code',
        'we dont get to play often and I hate my science teacher.'
    ]
    query_list = [
        # phone related
        'I wish best result in the test',
        'better academics will help me in brighter career',
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
        template_for_entry = prepare_template_for_insertion(student_name_age[i][1], student_name_age[i][0], sentences_list, embedding_vectors, i)
        insert_document(template_for_entry, index_name, i)
    """
    #############################################################################################

    """
    index_in_sentence_list= 5
    student_age = 23
    student_name = 'Sixth'
    template_for_entry = prepare_template_for_insertion(student_age, student_name, sentences_list, embedding_vectors, index_in_sentence_list)
    insert_document(template_for_entry, index_name, index_in_sentence_list)
    
    """
    
    ##############################################SEARCH######################################

    """
    top_n_results = 2
    
    #search results for the string "classes with mathematics numbers are so lame"#
    sentence_index = 3
    search_result, top_sentences = getSimilarVectors(index_name, top_n_results, sentence_index, q_embedding_vectors)
    """
    
    #####################COMPARISION##################################

    top_n_results = 2
    
    for i in range(len(query_list)):
        search_result, top_sentences = getSimilarVectors(index_name, top_n_results, i, q_embedding_vectors)
        print(query_list[i], end = '; ')
        print(top_sentences)
        print(' ')
    

    ##############################################EXTRA################################################################################
    """
    #index_name = "new_stud"
    #printDB(name)
    #vector = [0.63709, 9.0, 0.3322428, 0.4143116, 0.11339172, 0.40952107]
    #print(getSimilarVectors(index_name, 2, vector))
    #template_for_entry = {'age': 20, 'entry': datetime.now(), 'name': 'Harshavardhan', 'objective': 'we dont get to play often and I hate my science teacher.', 'sent_vec': embedding_vectors[0]}  
    #entry("new_stud", es, template_for_entry, 5)
    """

    
