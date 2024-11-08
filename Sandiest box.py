import urllib.request
import time
import os

# Set user agent and headers
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:132.0) Gecko/20100101 Firefox/132.0 '
headers = {'User-Agent': user_agent}


# Song title to scrape
i = "Lady_(Kenny_Rogers_song)"

# Define the URL
url = "https://en.wikipedia.org/wiki/Lady_(Kenny_Rogers_song)"

# Ensure the directory exists before saving the file
output_dir = '00 Billboards/wiki/page/'
os.makedirs(output_dir, exist_ok=True)

try:
    # Send the request
    request = urllib.request.Request(url, None, headers)
    response = urllib.request.urlopen(request)

    # Save the HTML content to a file
    with open(os.path.join(output_dir, f'{i}.html'), 'w', encoding="utf-8") as f:
        f.write(response.read().decode('utf-8'))

    print(f"Page saved as {i}.html")
    time.sleep(3)

except urllib.error.HTTPError as e:
    print(f"HTTP error occurred: {e}")
except urllib.error.URLError as e:
    print(f"URL error occurred: {e}")
