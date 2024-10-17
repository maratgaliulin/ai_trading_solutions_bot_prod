from urllib.request import urlretrieve
from PIL import Image
import os

def save_the_image(img_list:list) -> None:
    img_dir = 'methods/news_scraping/images/'
    img_name = img_list[0]
    img_url = img_list[1]
    urlretrieve(img_url, f"{img_dir}{img_name}.jpeg")
    py_img = Image.open(f"{img_dir}{img_name}.jpeg")
    py_img = py_img.resize((100,65))
    os.remove(f"{img_dir}{img_name}.jpeg")
    py_img.save(f"{img_dir}{img_name}.jpeg")