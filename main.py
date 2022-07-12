from text_extractors import necklaces, earrings, rings
from bots.acessorys import run_bot_acessory
import pymongo
import boto3
from dotenv import load_dotenv
import os
import shutil

load_dotenv()
mongo_client = pymongo.MongoClient('mongodb+srv://duanribeiro:BJ183r32@futebol-iwbwh.mongodb.net/imob?authSource=admin')
mongo_db = mongo_client["lostark"]
mongo_collection = mongo_db["prices"]
client = boto3.client(
    'rekognition',
    region_name='us-east-1',
    aws_access_key_id=os.getenv('ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('ACCESS_KEY_SECRET'),
)


def move_to_folder(SCREENSHOT_FOLDER, TOTAL_PAGES_CAPTURE):
    folder = ['', 'necklaces', 'earrings', 'rings']
    folder_index = 0

    for index, filename in enumerate(os.listdir(SCREENSHOT_FOLDER)):
        file_path = os.path.join(SCREENSHOT_FOLDER, filename)
        split_item = TOTAL_PAGES_CAPTURE * 11
        if index % split_item == 0:
            folder_index += 1
            folder_path = f'C:\\pics\\{folder[folder_index]}'

        shutil.move(file_path, folder_path)


if __name__ == "__main__":
    TOTAL_PAGES_CAPTURE = 30
    run_bot_acessory(TOTAL_PAGES_CAPTURE=TOTAL_PAGES_CAPTURE)

    SCREENSHOT_FOLDER = 'D:\SteamLibrary\steamapps\common\Lost Ark\EFGame\Screenshots'
    move_to_folder(SCREENSHOT_FOLDER=SCREENSHOT_FOLDER, TOTAL_PAGES_CAPTURE=TOTAL_PAGES_CAPTURE)
    mongo_collection.drop()
    necklaces.extract_data_from_image(client=client, mongo_collection=mongo_collection)
    earrings.extract_data_from_image(client=client, mongo_collection=mongo_collection)
    rings.extract_data_from_image(client=client, mongo_collection=mongo_collection)



