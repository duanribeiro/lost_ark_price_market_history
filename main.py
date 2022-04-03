import boto3
import cv2
import os
from datetime import datetime
import pytz
from dotenv import load_dotenv


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def get_created_time(image_path):
    image_asctime = os.path.getmtime(image_path)
    image_datetime = datetime.fromtimestamp(image_asctime).astimezone(pytz.utc)

    return image_datetime


def detect_text_local_file(image_path, folder_path):
    image = cv2.imread(image_path)
    cropped_image = image[220:690, 310:1350]
    cv2.imwrite(f'{folder_path}\\cropped.jpg', cropped_image)

    with open(f'{folder_path}\\cropped.jpg', 'rb') as image:
        response = client.detect_text(Image={'Bytes': image.read()})

    os.remove(f'{folder_path}\\cropped.jpg')
    return [text for text in response['TextDetections'] if text['Type'] == 'LINE']


def save_texts_db(texts, texts_datetime):
    clean_texts = []
    for text in texts:
        if 'Sold in bundles' not in text['DetectedText']:
            clean_texts.append(text['DetectedText'])

    parsed_text = []
    for chunk_text in list(chunks(clean_texts, 5)):
        parsed_item = {
            "name": chunk_text[0],
            "avg_day": float(chunk_text[1].replace(',', '')),
            "recent_price": float(chunk_text[2].replace(',', '')),
            "lowest_price": float(chunk_text[3].replace(',', '')),
            "cheapest_remaning": float(chunk_text[4].replace(',', '')),
            "timestamp": texts_datetime
        }
        print(parsed_item)
        parsed_text.append(parsed_item)


if __name__ == "__main__":
    load_dotenv()

    client = boto3.client(
        'rekognition',
        region_name='us-east-1',
        aws_access_key_id=os.getenv('ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('ACCESS_KEY_SECRET'),
    )

    screenshot_folder = 'C:\\pics'
    for filename in os.listdir(screenshot_folder):
        file_path = os.path.join(screenshot_folder, filename)

        if '.jpg' in file_path:
            image_datetime = get_created_time(image_path=file_path)
            detected_texts = detect_text_local_file(image_path=file_path, folder_path=screenshot_folder)
            save_texts_db(texts=detected_texts, texts_datetime=image_datetime)
