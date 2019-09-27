import ctypes
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import requests
import os

url = 'https://www.nasa.gov/rss/dyn/lg_image_of_the_day.rss'

r = requests.get(url)

lines = r.text.splitlines()

newpath = os.getcwd() + '/images/'

if not os.path.exists(newpath):
    os.makedirs(newpath)

for line in lines:
    if line[:32] == ' <link>http://www.nasa.gov/image':
        link = line[7:-7]
        re = requests.get(link, timeout=5)
        soup = BeautifulSoup(re.text, 'html.parser')
        for image in soup.find_all('meta'):
            if image.get('property') == 'og:image':
                global imagelink
                imagelink = image.get('content')
            else:
                pass
            if image.get('name') == 'dc.title':
                global title
                title = ''.join(c for c in image.get('content') if c.isalpha())
                print('Downloading Image: ' + title)
                
            else:
                pass
        dlim = requests.get(imagelink, allow_redirects=True)
        filename = title + '.jpg'
        open('images/' + filename, 'wb').write(dlim.content)
        print('\n')

    else:
        pass

print('All Images Downloaded')
print('Press enter to exit')
input()