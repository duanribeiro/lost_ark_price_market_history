import pymongo
import logging

mongo_client = pymongo.MongoClient('mongodb://mongoadmin:secret@localhost:27888/admin')
mongo_db = mongo_client["lostark"]
mongo_collection_builds = mongo_db["builds"]
mongo_collection_prices = mongo_db["prices"]

SCREENSHOT_FOLDER = 'D:\Steam\steamapps\common\Lost Ark\EFGame\Screenshots'
TESSERACT_EXE = r'D:\Program Files\Tesseract-OCR\tesseract.exe'
REGION_CONFIG_FILE = r'D:\Steam\steamapps\common\Lost Ark\EFGame\Config\UserOption.xml'

logging.basicConfig(filename='example.log', format='[%(asctime)s] %(message)s')
logger = logging.getLogger('market')
