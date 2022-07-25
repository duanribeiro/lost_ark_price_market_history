from bots.accessorys import run_bot_accessory
from text_extractor import extract_data_from_image
import pymongo

mongo_client = pymongo.MongoClient('mongodb+srv://duanribeiro:BJ183r32@futebol-iwbwh.mongodb.net/imob?authSource=admin')
mongo_db = mongo_client["lostark"]
mongo_collection = mongo_db["prices"]


if __name__ == "__main__":
    SCREENSHOT_FOLDER = 'D:\SteamLibrary\steamapps\common\Lost Ark\EFGame\Screenshots'
    run_bot_accessory(total_pages_capture=50)

    # mongo_collection.drop()
    # extract_data_from_image(screenshot_folder=SCREENSHOT_FOLDER, region='South America', mongo_collection=mongo_collection)
    # extract_data_from_image(screenshot_folder=SCREENSHOT_FOLDER, region='North America West', mongo_collection=mongo_collection)
    extract_data_from_image(screenshot_folder=SCREENSHOT_FOLDER, region='Central Europe', mongo_collection=mongo_collection)
