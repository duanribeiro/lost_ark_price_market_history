import cv2
import logging
import os
from helpers.utils import get_number_from_str


logging.basicConfig(format='[%(asctime)s] [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


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
       engraving_effect = string[1:].split(']')[0]
       response[engraving_effect] = get_number_from_str(string=string)

    return response


def detect_text_amazon_rekognition(client, image_path, folder_path):
    image = cv2.imread(image_path)
    start_x, end_x = 514, 723
    start_y, end_y = 220, 705

    cropped_image = image[start_y:end_y, start_x:end_x]
    cropped_image_gray = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)

    image_text = []
    cv2.imwrite(f'{folder_path}\\cropped_image.jpg', cropped_image_gray)
    with open(f'{folder_path}\\cropped_image.jpg', 'rb') as image:
        response = client.detect_text(Image={'Bytes': image.read()})
    os.remove(f'{folder_path}\\cropped_image.jpg')
    all_data_text = [text for text in response['TextDetections'] if text['Type'] == 'LINE']
    image_text += [text['DetectedText'] for text in all_data_text]

    return image_text


def clean_detected_texts(texts):
    # Descobrir os indices
    split_index = []
    for index, text in enumerate(texts):
        if any(word in text for word in ['Basic Effect', 'Bonus Effect', 'Random Engraving Effect']):
            split_index.append(index)
    new_texts = texts[split_index[0]:split_index[-1] + 4]

    for text in new_texts:
        if len(text) < 7:
            new_texts.remove(text)

        parsed_item = {
            "basic_effect": {
                "Strength": get_number_from_str(string=new_texts[1]),
                "Dexterity": get_number_from_str(string=new_texts[2]),
                "Intelligence": get_number_from_str(string=new_texts[3]),
                "Vitality": get_number_from_str(string=new_texts[4]),
            },
            "bonus_effect": get_number_from_bonus_effect(list=[new_texts[6]]),
            "engraving_effect": get_number_from_engraving_effect(list=new_texts[8:11]),
            "type": 'Rings',
        }

    return parsed_item
