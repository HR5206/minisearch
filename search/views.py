import os
import json
from django.shortcuts import render
from django.conf import settings
import crawler
import parser
import index as index_builder
import tfidf
import pagerank

CACHE_FILE = os.path.join(settings.BASE_DIR, 'data', 'crawled.json')
SEED_URLS = ['https://quotes.toscrape.com/']

if not os.path.exists(os.path.join(settings.BASE_DIR, 'data')):
    os.makedirs(os.path.join(settings.BASE_DIR, 'data'))

def load_or_crawl():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r', encoding='utf-8') as f:
            parsed_data = json.load(f)
    else:
        crawled_data = crawler.crawl(SEED_URLS, max_depth=2, max_pages=50)
        parsed_data = parser.parse(crawled_data)
        with open(CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(parsed_data, f)
    
    inverted_index, doc_lengths = index_builder.build_index(parsed_data)
    pr_scores = pagerank.compute_pagerank(parsed_data)
    return parsed_data, inverted_index, doc_lengths, pr_scores

parsed_data, inverted_index, doc_lengths, pr_scores = load_or_crawl()

def index(request):
    query = request.GET.get('q', '')
    results = []
    if query:
        num_docs = len(parsed_data)
        tfidf_scores = tfidf.compute_tfidf(query, inverted_index, doc_lengths, num_docs)
        
        combined_scores = []
        for url, t_score in tfidf_scores:
            p_score = pr_scores.get(url, 0)
            combined = t_score * p_score
            combined_scores.append((url, combined))
            
        combined_scores.sort(key=lambda x: x[1], reverse=True)
        
        for url, score in combined_scores:
            text = parsed_data[url]['text']
            query_terms = query.lower().split()
            snippet_start = 0
            for term in query_terms:
                idx = text.lower().find(term)
                if idx != -1:
                    snippet_start = max(0, idx - 20)
                    break
            snippet = text[snippet_start:snippet_start + 150]
            if len(text) > snippet_start + 150:
                snippet += "..."
                
            results.append({
                'url': url,
                'title': parsed_data[url]['title'],
                'score': score,
                'snippet': snippet
            })
            
    return render(request, 'search/index.html', {'query': query, 'results': results})
