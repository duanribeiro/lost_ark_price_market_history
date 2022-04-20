import boto3
from dotenv import load_dotenv
from datetime import datetime
import pytz
import cv2
import os
import logging
import pymongo

mongo_client = pymongo.MongoClient('mongodb+srv://duanribeiro:BJ183r32@futebol-iwbwh.mongodb.net/imob?authSource=admin')
mongo_db = mongo_client["lostark"]
mongo_collection = mongo_db["prices"]

logging.basicConfig(format='[%(asctime)s] [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def is_number(n):
    try:
        float(n)
    except ValueError:
        return False
    return True


def split_text_in_chunks(clean_texts):
    text_chunks = []
    chunk = []
    for text in clean_texts:
        text = text.replace(',', '.')
        if not is_number(text):
            text_chunks.append(chunk)
            chunk = [text]
        else:
            chunk.append(
                float(text)
            )
    text_chunks.append(chunk)

    return text_chunks[1:]


def get_created_time(image_path):
    image_asctime = os.path.getmtime(image_path)
    image_datetime = datetime.fromtimestamp(image_asctime).astimezone(pytz.utc)

    return image_datetime


def detect_text_local_file(client, image_path, folder_path):
    image = cv2.imread(image_path)
    height, width, channels = image.shape

    if height == 1080 and width == 1920:
        start_x, end_x = 610, 1630
        start_y, end_y = 300, 870

    elif height == 900 and width == 1600:
        start_x, end_x = 505, 1350
        start_y, end_y = 250, 730

    else:
        logger.error(f'Wrong image resolution: {width}x{height}. Only accepts 1920x1080 or 1600x900.')
        return None

    cropped_image = image[start_y:end_y, start_x:end_x]
    cv2.imwrite(f'{folder_path}\\cropped.jpg', cropped_image)
    with open(f'{folder_path}\\cropped.jpg', 'rb') as image:
        response = client.detect_text(Image={'Bytes': image.read()})

    os.remove(f'{folder_path}\\cropped.jpg')
    return [text for text in response['TextDetections'] if text['Type'] == 'LINE']


def save_texts_db(texts, texts_datetime):
    clean_texts = []
    save_list = []
    for text in texts:
        if not any(word in text['DetectedText'] for word in ['Sold in bundles', 'Untradable', 'May be traded']):
            clean_texts.append(text['DetectedText'])

    text_chunks = split_text_in_chunks(clean_texts)

    for chunk in text_chunks:
        if len(chunk) != 5:
            continue

        name, avg_day, recent_price, lowest_price, cheapest_remaning = chunk
        parsed_item = {
            "name": name,
            "avg_day": avg_day,
            "recent_price": recent_price,
            "lowest_price": lowest_price,
            "cheapest_remaning": cheapest_remaning,
            "timestamp": texts_datetime
        }
        logger.info(parsed_item)
        has_duplicated = list(mongo_collection.find({'name': parsed_item['name'], 'timestamp': parsed_item['timestamp']}))
        if not has_duplicated:
            save_list.append(parsed_item)

    logger.info(f'Itens on page: {len(text_chunks)}')
    logger.info(f'Itens to be saved: {len(save_list)}')
    mongo_collection.insert_many(save_list)


if __name__ == "__main__":
    logger.info(f'Starting...')
    load_dotenv()

    client = boto3.client(
        'rekognition',
        region_name='us-east-1',
        aws_access_key_id=os.getenv('ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('ACCESS_KEY_SECRET'),
    )

    screenshot_folder = 'C:\\pics'
    logger.info(f'Starting read images on folder: {screenshot_folder}')

    try:
        os.listdir(screenshot_folder)
    except:
        logger.error(f'Pasta não encontrada: {screenshot_folder}')
        quit()

    for filename in os.listdir(screenshot_folder):
        file_path = os.path.join(screenshot_folder, filename)
        logger.info(f'Reading image: {filename}')

        if '.jpg' in file_path:
            image_datetime = get_created_time(image_path=file_path)
            detected_texts = detect_text_local_file(client=client, image_path=file_path, folder_path=screenshot_folder)
            if detected_texts:
                save_texts_db(texts=detected_texts, texts_datetime=image_datetime)

    input("Press any key to exit...")

