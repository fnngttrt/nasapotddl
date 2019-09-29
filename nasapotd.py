from bs4 import BeautifulSoup
import requests
import os


def get_image_pages():
    url = 'https://www.nasa.gov/rss/dyn/lg_image_of_the_day.rss'
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    results = []
    for item in soup.findAll('item'):
        image_url = item.find('enclosure')['url']
        image_extension = os.path.splitext(image_url)[-1]
        image_title = item.find('title').text.replace(':', ' -').replace('"', '')  # We replace problematic characters
        results.append({'url': image_url, 'title': image_title + image_extension})
    return results


def download_one_image(url, save_path):
    r = requests.get(url)
    with open(save_path, 'wb') as f:
        f.write(r.content)


def download_all_images(save_folder_path):
    os.makedirs(save_folder_path, exist_ok=True)
    images = get_image_pages()
    for i, img in enumerate(images):
        img_path = os.path.join(save_folder_path, img['title'])
        if not os.path.isfile(img_path):  # So we don't download and overwrite the same thing twice, ever
            print('Downloading image ' + str(i) + '/' + str(len(images)) + ': ' + img_path)
            download_one_image(img['url'], img_path)


if __name__ == '__main__':
    download_all_images('images')
    print('All Images Downloaded')
    print('Press enter to exit')
    input()
