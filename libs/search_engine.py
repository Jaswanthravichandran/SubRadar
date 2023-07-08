from googlesearch import search

def query_search_engine(domain):
    subdomains = set()
    query = f'site:{domain}'
    num_results = 10  # Adjust the number of search results to retrieve

    # Perform the search query and process the results
    for result in search(query, num_results=num_results, stop=num_results, pause=2):
        subdomain = extract_subdomain(result)
        if subdomain:
            subdomains.add(subdomain)

    return subdomains

def extract_subdomain(url):
    # Extracts the subdomain from a URL
    # Customize this function based on your target domain structure
    # Example: Extracts subdomain from "http://subdomain.example.com/path"
    # Result: "subdomain.example.com"
    if '//' in url:
        url = url.split('//', 1)[1]
    subdomain = url.split('/', 1)[0]
    return subdomain

# Usage example
if __name__ == '__main__':
    domain_name = 'example.com'
    subdomains = query_search_engine(domain_name)
    print("Discovered subdomains:")
    for subdomain in subdomains:
        print(subdomain)
