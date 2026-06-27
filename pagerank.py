def compute_pagerank(parsed_data, iterations=50, damping=0.85):
    urls = list(parsed_data.keys())
    num_urls = len(urls)
    if num_urls == 0:
        return {}
        
    pagerank = {url: 1.0 / num_urls for url in urls}
    
    outbound_links = {}
    for url, data in parsed_data.items():
        valid_links = [link for link in data["links"] if link in urls]
        outbound_links[url] = valid_links
        
    for _ in range(iterations):
        new_pagerank = {}
        for url in urls:
            rank_sum = 0
            for other_url, links in outbound_links.items():
                if url in links:
                    rank_sum += pagerank[other_url] / len(links)
            new_pagerank[url] = (1 - damping) / num_urls + damping * rank_sum
        pagerank = new_pagerank
        
    return pagerank
