# minisearch

built this over the weekend because i wanted to see how hard it actually is to make a search engine from scratch. tbh it's not that deep but the math for pagerank was kinda annoying.

it has 6 parts, all written in pure python without any crazy ML libraries. no sklearn, no NLTK, nothing. just raw algorithms.

## what it does
1. **crawler**: scrapes some seed urls (currently hardcoded to a quotes site because i didn't want to get ip banned testing it). 
2. **parser**: strips out all the html junk and script tags using beautifulsoup.
3. **inverted index**: tokenizes stuff, drops stopwords, and builds a massive dict.
4. **tf-idf**: calculates term frequency-inverse document frequency from scratch. 
5. **pagerank**: iterative power method to rank the links. (damping factor is 0.85, don't change it unless you know what you're doing).
6. **ui**: wired the whole thing up in django.

## how to run

make sure you have django, requests, and beautifulsoup4 installed.

```bash
pip install django requests beautifulsoup4
```

then just start the server:

```bash
python manage.py runserver
```

it will hang for like 15 seconds the first time you run it because it's actively crawling the internet and building the index. it saves a `crawled.json` cache file in `/data` so subsequent reloads are instant. if you want to crawl different sites, delete the cache file and change the `SEED_URLS` in `search/views.py`.

## notes
- no css frameworks. pure custom styling.
- i didn't write any comments because the code is self-documenting lol.
- if it crashes on windows, idk it works on my machine. 
