import urllib.request
import urllib.error
import time
from bs4 import BeautifulSoup

baseUrl = "https://en.wikipedia.org/w/index.php?title=Category:Billboard_Hot_100_number-one_singles&from="

# Creating a list of letters from the alphabet:
urlSuffixList = list(map(chr, range(ord('A'), ord('Z') + 1)))

# Adding zero as a string to the beginning of the list
urlSuffixList.insert(0, '0')

# Creating empty list to hold urls to scrape:
urlList = list()

# Appending suffixes to URLs:
for item in urlSuffixList:
    urlList.append(baseUrl + str(item))

# Setup user-agent header for making requests
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:132.0) Gecko/20100101 Firefox/132.0'
headers = {'User-Agent': user_agent}

# Inroduce empty list to append scraped urls to
urls_to_scrape =[]

# Iterate over the generated URLs in urlList
for url in urlList:
    try:
        # Make the request with the custom User-Agent header
        request = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(request)
        
        # Parse the HTML content of the response using BeautifulSoup
        soup = BeautifulSoup(response.read(), "lxml")

        # Find the first category group containing the links
        category_group = soup.find("div", {"class": "mw-category-group"})

        # If the category group is found, process the links
        if category_group:
            links = category_group.find_all('a')
            for link in links:
                href = link.get('href')
                if href:  # Only process if href exists
                    full_url = "https://en.wikipedia.org" + href
                    urls_to_scrape.append(full_url)
                    print(full_url)
        else:
            print(f"Category group not found for URL: {url}")

        # Wait to avoid carmic debt
        time.sleep(1)

    except urllib.error.HTTPError as e:
        print(f"HTTPError: {e.code} for URL: {url}")

