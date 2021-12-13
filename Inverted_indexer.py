
def generate_inverted_index():
    with open('forward_index.txt', 'r+') as fwd_idx:
            for object in fwd_idx:
                document = json.loads(object)
                doc_ids.add(document['docID'])

