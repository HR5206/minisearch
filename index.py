import string

STOPWORDS = {"a", "an", "and", "are", "as", "at", "be", "but", "by", "for", "if", "in", "into", "is", "it", "no", "not", "of", "on", "or", "such", "that", "the", "their", "then", "there", "these", "they", "this", "to", "was", "will", "with"}

def build_index(parsed_data):
    inverted_index = {}
    doc_lengths = {}
    
    for url, data in parsed_data.items():
        text = data["text"].lower()
        translator = str.maketrans("", "", string.punctuation)
        text = text.translate(translator)
        tokens = text.split()
        
        filtered_tokens = [t for t in tokens if t not in STOPWORDS]
        doc_lengths[url] = len(filtered_tokens)
        
        for token in filtered_tokens:
            if token not in inverted_index:
                inverted_index[token] = {}
            if url not in inverted_index[token]:
                inverted_index[token][url] = 0
            inverted_index[token][url] += 1
            
    return inverted_index, doc_lengths
