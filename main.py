import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import sys

visited_urls = set()

def get_sub_sites_and_images(base_url, file, max_depth=2, current_depth=0):
    if current_depth > max_depth:
        return

    try:
        response = requests.get(base_url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to fetch {base_url}: {e}", file=sys.stderr)
        return

    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract all links
    links = soup.find_all('a', href=True)
    
    # Extract all image sources
    images = soup.find_all('img', src=True)

    # Process each link
    for link in links:
        href = link['href']
        full_url = urljoin(base_url, href)

        if is_same_domain(base_url, full_url):
            if full_url not in visited_urls:
                visited_urls.add(full_url)
                print(f"Sub-site: {full_url}")
                file.write(f"Sub-site: {full_url}\n")
                get_sub_sites_and_images(full_url, file, max_depth, current_depth + 1)

    # Process each image
    for image in images:
        img_src = image['src']
        full_img_url = urljoin(base_url, img_src)
        print(f"Image: {full_img_url}")
        file.write(f"Image: {full_img_url}\n")

def is_same_domain(base_url, url):
    base_domain = urlparse(base_url).netloc
    target_domain = urlparse(url).netloc
    return base_domain == target_domain

if __name__ == "__main__":
    base_url = "https://open-api.choiceqr.com"
    max_depth = 2  # You can change this value based on how deep you want to crawl
    
    with open("sub_sites_and_images.txt", "w") as file:
        get_sub_sites_and_images(base_url, file, max_depth)
    
    print("Sub-sites and image links have been saved to sub_sites_and_images.txt.")
