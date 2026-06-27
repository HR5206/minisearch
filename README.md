# minisearch

wanted to understand how search engines actually work under the hood, so i built one. no shortcuts —
the crawler, index, ranking, and UI are all written from scratch in pure python.

## what it does

1. **crawler** — BFS crawl from seed URLs, respects robots.txt, saves raw HTML to disk
2. **parser** — strips HTML noise with beautifulsoup, extracts clean text and outbound links
3. **inverted index** — tokenizes text, removes stopwords, maps tokens → (doc_id, positions)
4. **tf-idf** — scores documents against a query using term frequency × inverse document frequency
5. **pagerank** — iterative power method over the link graph, damping factor 0.85 (the value from
   the original Brin & Page paper). ranks pages by how many other pages link to them.
6. **django UI** — search form, ranked results, and snippet previews wired together

## sample output

```
query: "albert einstein"

1. [0.91] quotes.toscrape.com/author/Albert-Einstein
2. [0.44] quotes.toscrape.com/page/3/
3. [0.19] quotes.toscrape.com/tag/inspirational/
```

## how to run

```bash
pip install django requests beautifulsoup4
python manage.py runserver
```

first load takes ~15 seconds — it crawls the seed URLs and builds the index, then caches
everything to `data/crawled.json`. subsequent loads are instant. to re-crawl, delete the
cache file and update `SEED_URLS` in `search/views.py`.

## technical notes

- inverted index lookup is O(1). full query ranking is O(n log n) where n = matching documents.
- pagerank converges in ~30 iterations for a 50-page graph.
- tested on macOS and Linux. no external ML libraries used anywhere.