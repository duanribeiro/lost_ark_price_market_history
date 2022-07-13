
from datetime import datetime
import pytz
import os
import logging
from text_extractors import window_data, necklace_helpers

logging.basicConfig(format='[%(asctime)s] [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def get_created_time(image_path):
    image_asctime = os.path.getmtime(image_path)
    image_datetime = datetime.fromtimestamp(image_asctime).astimezone(pytz.utc)

    return image_datetime


def extract_data_from_image(client, mongo_collection):
    screenshot_folder = r'C:\pics\necklaces'
    logger.info(f'Starting read images on folder: {screenshot_folder}')

    for index, filename in enumerate(os.listdir(screenshot_folder)):
        file_path = os.path.join(screenshot_folder, filename)
        logger.info(f'Reading image: {filename}')
        image_datetime = get_created_time(image_path=file_path)

        if index % 11 == 0:
            window_item_relation = 0
            detected_texts = window_data.detect_text_amazon_rekognition(
                client=client, image_path=file_path, folder_path=screenshot_folder
            )
            parsed_items_window = window_data.clean_detected_texts(
                texts=detected_texts, texts_datetime=image_datetime
            )

        else:
            try:
                detected_item_texts = necklace_helpers.detect_text_amazon_rekognition(
                    client=client, image_path=file_path, folder_path=screenshot_folder
                )
                parsed_items = necklace_helpers.clean_detected_texts(texts=detected_item_texts)
                # result_all_itens.append({**parsed_items_window[window_item_relation], **parsed_items})
                mongo_collection.insert({**parsed_items_window[window_item_relation], **parsed_items})
                window_item_relation += 1
            except Exception as e:
                logger.error(f'Erro na imagem: {e}')
                window_item_relation += 1
