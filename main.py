from forward_indexer import generate_forward_index
from inverted_indexer import inverted_index_generator

# provide path to directory which contains json files (dataset)
# creates forward index, lexicon and document index
generate_forward_index('./Dataset/nela-gt-2020/newsdata')
# creates inverted index out of forward barrels
inverted_index_generator()
