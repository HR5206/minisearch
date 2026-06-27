import math

def compute_tfidf(query, inverted_index, doc_lengths, num_docs):
    query = query.lower().split()
    scores = {}
    
    for term in query:
        if term in inverted_index:
            doc_freq = len(inverted_index[term])
            idf = math.log(num_docs / doc_freq) if doc_freq > 0 else 0
            
            for url, term_freq in inverted_index[term].items():
                if doc_lengths[url] > 0:
                    tf = term_freq / doc_lengths[url]
                    if url not in scores:
                        scores[url] = 0
                    scores[url] += tf * idf
                
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)
