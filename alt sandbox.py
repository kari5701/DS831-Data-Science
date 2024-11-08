import urllib.request
import urllib.error
import time
import os

baseUrl = "https://en.wikipedia.org/w/index.php?title=Category:Billboard_Hot_100_number-one_singles&from="

# Creating a list of letters from the alphabet:
urlSuffixList = list(map(chr, range(ord('A'), ord('Z') + 1)))

# Adding zero as an int to the beginning of the list
urlSuffixList.insert(0, int(0))

urlList = list()

for item in urlSuffixList:
    urlList.append(baseUrl + str(item))

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:132.0) Gecko/20100101 Firefox/132.0'
headers = {'User-Agent': user_agent}

# Create a "wiki" folder if it doesn't exist
if not os.path.exists('wiki'):
    os.makedirs('wiki')


# I got errors when writing full url as filename, so i decided to use just the last charecter:

def last_url_char(url):
    # Extract the last character after the '=' in the URL
    return url.split('=')[-1]

for i in urlList:
    try:
        request = urllib.request.Request(i, None, headers)
        response = urllib.request.urlopen(request)
        
        # Extract the last character from the URL
        last_char = last_url_char(i)
        
        # Create a filename based on the last character
        file_name = f"listpage_{last_char}.html"
        file_path = os.path.join("wiki", file_name)
        
        # Write the HTML content to the file
        with open(file_path, 'w', encoding="utf-8") as f:
            f.write(str(response.read().decode('utf-8')))
        
        time.sleep(1)
    
    except urllib.error.HTTPError as e:
        print(f"HTTPError: {e.code} for URL: {i}")
    except urllib.error.URLError as e:
        print(f"URLError: {e.reason} for URL: {i}")
    except Exception as e:
        print(f"An error occurred: {e}")
