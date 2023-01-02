import os
from PIL import Image
from settings import mongo_collection_prices, SCREENSHOT_FOLDER, logger
from helpers import extract_item_name, extract_traded_times, extract_quality, \
    extract_time_left, extract_minimum_bid, extract_buy_now, \
    extract_description, get_created_time, discover_item_type


# cropped_image.save('test.jpg', quality=100, subsampling=0)


def extract_data_from_image(region):
    counter = 0
    for index, filename in enumerate(os.listdir(SCREENSHOT_FOLDER)):
        file_path = os.path.join(SCREENSHOT_FOLDER, filename)
        timestamp = get_created_time(image_path=file_path)
        image = Image.open(file_path)
        gray_image = image.convert("L")

        if index % 11 == 0:
            logger.warning(f'{filename} [*]')
            parsed_items = []
            window_item_relation = 0
            start_x, end_x = 552, 1602
            start_y = 306
            for item in range(0, 10):
                cropped_image = gray_image.crop((start_x, start_y, end_x, start_y + 58))

                item_name = extract_item_name(image=cropped_image)
                minimum_bid = extract_minimum_bid(image=cropped_image)
                buy_now = extract_buy_now(image=cropped_image)
                traded_times = extract_traded_times(image=cropped_image)
                time_left = extract_time_left(image=cropped_image)
                quality = extract_quality(image=cropped_image)

                parsed_items.append({
                    "name": item_name,
                    # "item_lv": 'Tier 3',
                    "region": region,
                    "minimum_bid": minimum_bid,
                    "buy_now_price": buy_now,
                    "traded_times": traded_times,
                    "time_left": time_left,
                    "quality": quality,
                    "timestamp": timestamp,
                    "type": discover_item_type(item_name=item_name),
                })
                start_y += 57
        else:
            logger.warning(f'[{counter}] {filename}')
            start_x, end_x = 725, 1020
            start_y, end_y = 300, 1015
            cropped_image = gray_image.crop((start_x, start_y, end_x, end_y))
            description = extract_description(image=cropped_image)
            result = {**parsed_items[window_item_relation], **description}
            mongo_collection_prices.insert_one(result)
            window_item_relation += 1
            counter += 1



