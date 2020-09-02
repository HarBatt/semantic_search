# semantic_search

### Requirements
- Tensorflow 1.x
- Elasticsearch, Kibana, BERT client
- Start elasticsearch and BERT client from cmd using (bert-serving-start -model_dir C:xxxxxxxxx\bert\cased_L-12_H-768_A-12 -num_worker= 1).


Use ```create_index.py``` to create index and to change it's mappings.

Multifield search is performed using the mappings shown in ```current_mappings.png```

Custom static mappings can be defined using ```create_index.py``` and include the same in ```multifield_search.py```  before performing the search. 
