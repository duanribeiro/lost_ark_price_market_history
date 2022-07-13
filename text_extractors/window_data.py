import cv2
import logging
import os
from helpers.utils import get_number_from_str


logging.basicConfig(format='[%(asctime)s] [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def detect_text_amazon_rekognition(client, image_path, folder_path):
    image = cv2.imread(image_path)
    start_x, end_x = 435, 1158
    start_y, end_y = 220, 622

    cropped_image = image[start_y:end_y, start_x:end_x]
    cropped_image_gray = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)

    cropped_image_gray_first_half = cropped_image_gray[0:201, 0:723]
    cropped_image_gray_second_half = cropped_image_gray[202:402, 0:723]

    image_text = []
    for cropped_image in [cropped_image_gray_first_half, cropped_image_gray_second_half]:
        cv2.imwrite(f'{folder_path}\\cropped_image.jpg', cropped_image)
        with open(f'{folder_path}\\cropped_image.jpg', 'rb') as image:
            response = client.detect_text(Image={'Bytes': image.read()})
        os.remove(f'{folder_path}\\cropped_image.jpg')
        all_data_text = [text for text in response['TextDetections'] if text['Type'] == 'LINE']
        image_text += [text['DetectedText'] for text in all_data_text]

    return image_text


def clean_detected_texts(texts, texts_datetime):
    # Descobrir o tamanho da lista que tem os dados apenas de um item
    split_index = []
    for index, text in enumerate(texts):
        if any(word in text for word in ['Earrings', 'Ring', 'Necklace']) and index != 0:
            split_index.append(index)
    items = []
    start_index = 0
    for split in split_index:
        end_index = split
        items.append(
            texts[start_index:end_index]
        )
        start_index = end_index
    items.append(
        texts[split_index[-1]:]
    )

    # Caso tenha apenas 6 valores, significa que o buy_now_price não existe
    parsed_items_window = []
    for item in items:
        if len(item) >= 6:
            last = item[-1]
            item = [x for x in item[:-1] if len(x) >= 2]
            item.append(last)
        if 'adidas' in item:
            item.remove('adidas')

        ending_soon = False
        if 'Ending Soon' in item:
            ending_soon = True

        if ending_soon:
            if len(item) < 7:
                parsed_item = {
                    "name": item[0],
                    "item_lv": item[2],
                    "minimum_bid": int(item[3].replace(',', '').replace('.', '')),
                    "buy_now_price": None,
                    "traded_times": get_number_from_str(string=item[4]),
                    "time_left": item[5],
                    "quality": int(item[6]),
                    "timestamp": texts_datetime
                }
            else:
                try:
                    parsed_item = {
                        "name": item[0],
                        "item_lv": item[2],
                        "minimum_bid": int(item[3].replace(',', '').replace('.', '')),
                        "buy_now_price": int(item[4].replace(',', '').replace('.', '')),
                        "traded_times": get_number_from_str(string=item[5]),
                        "time_left": item[6],
                        "quality": int(item[7]),
                        "timestamp": texts_datetime
                    }
                except:
                    parsed_item = {
                        "name": item[0],
                        "item_lv": item[2],
                        "minimum_bid": int(item[3].replace(',', '').replace('.', '')),
                        "buy_now_price": None,
                        "traded_times": get_number_from_str(string=item[4]),
                        "time_left": item[5],
                        "quality": int(item[6]),
                        "timestamp": texts_datetime
                    }

        elif len(item) < 7:
            parsed_item = {
                "name": item[0],
                "item_lv": item[1],
                "time_left": item[2],
                "minimum_bid": int(item[3].replace(',', '').replace('.', '')),
                "buy_now_price": None,
                "traded_times": get_number_from_str(string=item[4]),
                "quality": int(item[5]),
                "timestamp": texts_datetime
            }
        else:
            try:
                parsed_item = {
                    "name": item[0],
                    "item_lv": item[1],
                    "time_left": item[2],
                    "minimum_bid": int(item[3].replace(',', '').replace('.', '')),
                    "buy_now_price": int(item[4].replace(',', '').replace('.', '')),
                    "traded_times": get_number_from_str(string=item[5]),
                    "quality": int(item[6]),
                    "timestamp": texts_datetime
                }
            except:
                parsed_item = {
                    "name": item[0],
                    "item_lv": item[1],
                    "time_left": item[2],
                    "minimum_bid": int(item[3].replace(',', '').replace('.', '')),
                    "buy_now_price": None,
                    "traded_times": get_number_from_str(string=item[4]),
                    "quality": int(item[5]),
                    "timestamp": texts_datetime
                }

        parsed_items_window.append(parsed_item)
    return parsed_items_window
