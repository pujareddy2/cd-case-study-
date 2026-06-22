import urllib.request
import re

html = urllib.request.urlopen('https://www.stanley.edu.in/').read().decode('utf-8')
matches = re.findall(r'src=["\']([^"\']*logo[^"\']*png)["\']', html, re.I)
if matches:
    url = matches[0]
    if url.startswith('/'):
        url = 'https://www.stanley.edu.in' + url
    print("Found logo URL:", url)
    urllib.request.urlretrieve(url, 'logo.png')
    print("Downloaded to logo.png")
else:
    print("No logo found.")
