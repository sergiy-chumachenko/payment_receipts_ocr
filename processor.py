from PIL import Image
from wand.image import Image as WandImage
from pyocr import pyocr
from datetime import datetime
import os
import codecs

from django.conf import settings
from ez_claims.settings.base import STATIC_ROOT

BASE_DIR = os.path.abspath(os.curdir)


def processing(path_to_image, filename, user):
    directory_for_input_data = BASE_DIR + '/ocr/ocr_input_data/{}/'.format(user)
    if not os.path.exists(directory_for_input_data):
        os.makedirs(directory_for_input_data)
    if filename[-3:] == 'pdf':
        filename = filename[:-4]
        with WandImage(filename=settings.STATIC_ROOT+path_to_image) as img:
            img.save(filename="{}/{}.jpg".format(directory_for_input_data, filename))
    elif filename[-3:] == 'png':
        filename = filename[:-4]
        img = Image.open(fp=STATIC_ROOT+path_to_image)
        rgb_im = img.convert('RGB')
        rgb_im.save('{}/{}.jpg'.format(directory_for_input_data, filename), 'JPEG')
    else:
        filename = filename[:-4]
        img = Image.open(fp=STATIC_ROOT+path_to_image)
        img.save('{}/{}.jpg'.format(directory_for_input_data, filename), 'JPEG')

    tools = pyocr.get_available_tools()
    tool = tools[0]
    date = str(datetime.today())[:-7].replace('-', '_').replace(' ', '__').replace(':', '_')
    text = tool.image_to_string(Image.open("{}/{}.jpg".format(directory_for_input_data, filename)))
    directory_for_results = BASE_DIR + '/ocr/ocr_results/{}/'.format(user)
    if not os.path.exists(directory_for_results):
        os.makedirs(directory_for_results)
    filename = 'res_{}_{}.txt'.format(filename, date)
    with codecs.open(directory_for_results+filename, 'a', encoding='utf-8') as txt_file:
        txt_file.write(text)
    return directory_for_results+filename
