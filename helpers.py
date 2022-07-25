import pytesseract
from PIL import ImageFilter
import re
import os
from datetime import datetime
import pytz
from names import engravings_names
import difflib
import logging

pytesseract.pytesseract.tesseract_cmd = r'D:\Program Files\Tesseract-OCR\tesseract.exe'
logging.basicConfig(format='[%(asctime)s] [%(levelname)s] %(message)s')


def check_engraving_name(text):
    engraving_name = difflib.get_close_matches(text, engravings_names)
    if engraving_name:
        return engraving_name[0]
    return text


def get_created_time(image_path):
    image_asctime = os.path.getmtime(image_path)
    image_datetime = datetime.fromtimestamp(image_asctime).astimezone(pytz.utc)

    return image_datetime


def get_number_from_str(string):
    temp = re.findall(r'\d+', string)
    res = list(map(int, temp))
    return res[0] if res else 0


def get_number_from_bonus_effect(list):
    response = {}
    for string in list:
        if 'Crit' in string:
            bonus_effect = 'Crit'
        elif 'Specialization' in string:
            bonus_effect = 'Specialization'
        elif 'Domination' in string:
            bonus_effect = 'Domination'
        elif 'Swiftness' in string:
            bonus_effect = 'Swiftness'
        elif 'Endurance' in string:
            bonus_effect = 'Endurance'
        elif 'Expertise' in string:
            bonus_effect = 'Expertise'

        response[bonus_effect] = get_number_from_str(string=string)

    return response


def get_number_from_engraving_effect(list):
    response = {}
    for string in list:
        if string:
           engraving_effect = string.split('Node')[0].replace(',', '.').replace('[', '').replace(']', '').strip()
           engraving_effect = check_engraving_name(text=engraving_effect)
           response[engraving_effect] = get_number_from_str(string=string)

    return response


def discover_item_type(item_name):
    if 'Necklace' in item_name:
        type = 'Necklace'
    elif 'Earring' in item_name:
        type = 'Earring'
    elif 'Ring' in item_name:
        type = 'Ring'
    else:
        type = None

    return type


def extract_item_name(image):
    start_x, end_x = 60, 240
    start_y, end_y = 7, 25
    cropped_image = image.crop((start_x, start_y, end_x, end_y))
    sharpened = cropped_image.filter(ImageFilter.SHARPEN)
    binarie_image = sharpened.point(lambda x: 0 if x > 55 else 1, "1")
    text = pytesseract.image_to_string(binarie_image, config='--psm 7')
    clean_text = re.sub(r'\W+', ' ', text).strip()
    return clean_text


def extract_traded_times(image):
    start_x, end_x = 60, 240
    start_y, end_y = 29, 45
    cropped_image = image.crop((start_x, start_y, end_x, end_y))
    sharpened = cropped_image.filter(ImageFilter.SHARPEN)
    binarie_image = sharpened.point(lambda x: 0 if x > 80 else 1, "1")
    text = pytesseract.image_to_string(binarie_image, config='--psm 7')
    clean_text = get_number_from_str(text)
    return clean_text


def extract_quality(image):
    start_x, end_x = 500, 530
    start_y, end_y = 29, 50
    cropped_image = image.crop((start_x, start_y, end_x, end_y))
    sharpened = cropped_image.filter(ImageFilter.SHARPEN)
    binarie_image = sharpened.point(lambda x: 0 if x > 30 else 1, "1")
    text = pytesseract.image_to_string(binarie_image, config='--psm 7')
    clean_text = get_number_from_str(text)
    return clean_text


def extract_time_left(image):
    start_x, end_x = 625, 715
    start_y, end_y = 10, 45
    cropped_image = image.crop((start_x, start_y, end_x, end_y))
    sharpened = cropped_image.filter(ImageFilter.SHARPEN)
    binarie_image = sharpened.point(lambda x: 0 if x > 30 else 1, "1")
    text = pytesseract.image_to_string(binarie_image, config='--psm 7').strip()

    return text


def extract_minimum_bid(image):
    start_x, end_x = 790, 879
    start_y, end_y = 10, 45
    cropped_image = image.crop((start_x, start_y, end_x, end_y))
    sharpened = cropped_image.filter(ImageFilter.SHARPEN)

    no_valid_number = True
    scale_x = 30
    while no_valid_number:
        binarie_image = sharpened.point(lambda x: 0 if x > scale_x else 1, "1")
        text = pytesseract.image_to_string(binarie_image, config='--psm 7').strip()
        try:
            text = int(text.replace(',', '').replace('.', ''))
            no_valid_number = False
        except ValueError as e:
            logging.error(f'Adjusting extract_minimum_bid scale_x to: {scale_x}')
            scale_x += 5
            if scale_x >= 100:
                return None

    return text


def extract_buy_now(image):
    start_x, end_x = 960, 1050
    start_y, end_y = 10, 45
    cropped_image = image.crop((start_x, start_y, end_x, end_y))
    sharpened = cropped_image.filter(ImageFilter.SHARPEN)

    no_valid_number = True
    scale_x = 30
    while no_valid_number:
        binarie_image = sharpened.point(lambda x: 0 if x > scale_x else 1, "1")
        text = pytesseract.image_to_string(binarie_image, config='--psm 7').strip()
        if text == '-':
            return None
        try:
            text = int(text.replace(',', '').replace('.', ''))
            no_valid_number = False
        except ValueError as e:
            logging.error(f'Adjusting extract_buy_now scale_x to: {scale_x}')
            scale_x += 5
            if scale_x >= 100:
                return None
    return text


def extract_description(image):
    sharpened = image.filter(ImageFilter.SHARPEN)
    binarie_image = sharpened.point(lambda x: 0 if x > 60 else 1, "1")
    text = pytesseract.image_to_string(binarie_image)

    try:
        restricted_level_text = text.split('Basic Effect')[0].split('Level')[1].strip()
        restricted_level = get_number_from_str(string=restricted_level_text)
    except:
        restricted_level = None
    # basic_effect = text.split('Basic Effect')[1].split('Bonus Effect')[0].strip().split('+')
    basic_effect = text.split('Basic Effect')[1].split('Bonus Effect')[0].strip().split('\n')
    bonus_effect = text.split('Bonus Effect')[1].split('Random Engraving Effect')[0].strip().split('\n')
    engraving_effect = text.split('Random Engraving Effect')[1].split("Can't upgrade quality")[0].strip().split('\n')

    description = {
        "restricted_level": restricted_level,
        "basic_effect": {
            "Strength": get_number_from_str(string=basic_effect[0]),
            "Dexterity": get_number_from_str(string=basic_effect[1]),
            "Intelligence": get_number_from_str(string=basic_effect[2]),
            "Vitality": get_number_from_str(string=basic_effect[3]),
        },
        "bonus_effect": get_number_from_bonus_effect(list=bonus_effect),
        "engraving_effect": get_number_from_engraving_effect(list=engraving_effect),
    }

    return description
