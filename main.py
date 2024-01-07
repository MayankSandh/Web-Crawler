import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

def get_links(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        links = [link.get('href') for link in soup.find_all('a', href=True)]
        return links
    except requests.RequestException as e:
        print("Error fetching page:", e)
        return []

def categorize_links(links):
    categorized_links = {}
    for link in links:
        parsed_link = urlparse(link)
        if parsed_link.path:
            extension = parsed_link.path.split('.')[-1]
            if extension not in categorized_links:
                categorized_links[extension] = [link]
            else:
                categorized_links[extension].append(link)
    return categorized_links

def crawl(url, depth=2):
    visited = set()
    queue = [(url, 0)]

    while queue:
        current_url, current_depth = queue.pop(0)
        if current_depth > depth:
            break

        if current_url not in visited:
            visited.add(current_url)
            print(f"Crawling: {current_url}")
            links = get_links(current_url)
            categorized_links = categorize_links(links)
            
            # Print categorized links
            for extension, categorized in categorized_links.items():
                print(f"Links with extension '{extension}':")
                for link in categorized:
                    print(link)
                print()

            # Add new links to the queue
            for link in links:
                if link.startswith('http') and urlparse(link).netloc == urlparse(url).netloc:
                    queue.append((link, current_depth + 1))

# Example usage:
crawl('https://en.wikipedia.org/wiki/Daisy_Bacon', depth=1)
