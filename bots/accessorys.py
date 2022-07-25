import logging
from time import sleep

import pyautogui

logging.basicConfig(format='[%(asctime)s][%(levelname)s] %(message)s')


def click_category_accessory():
    logging.warning('Clicking on acessory')
    pyautogui.moveTo(x=310, y=401, duration=1)
    pyautogui.click(x=310, y=401, duration=1)
    sleep(2)


def click_subcategory_neklaces():
    logging.warning('Clicking on necklace')
    pyautogui.moveTo(x=310, y=482, duration=1)
    pyautogui.click(x=310, y=482, duration=1)
    sleep(2)


def click_subcategory_earrings():
    logging.warning('Clicking on earrings')
    pyautogui.moveTo(x=310, y=522, duration=1)
    pyautogui.click(x=310, y=522, duration=1)
    sleep(2)


def click_subcategory_rings():
    logging.warning('Clicking on rings')
    pyautogui.moveTo(x=310, y=561, duration=1)
    pyautogui.click(x=310, y=561, duration=1)
    sleep(2)


def click_order_desc_bid():
    logging.warning('Clicking on ordering descending bid')
    pyautogui.moveTo(x=1380, y=283, duration=1)
    pyautogui.click(x=1380, y=283, duration=1)
    sleep(2)


def click_next_page():
    logging.warning('Clicking on next page')
    pyautogui.moveTo(x=1143, y=899, duration=1)
    pyautogui.click(x=1143, y=899, duration=1)
    sleep(2)


def run_bot_necklaces(total_pages_capture):
    logging.warning('Starting Necklaces...')
    sleep(5)
    click_category_accessory()
    click_subcategory_neklaces()
    click_order_desc_bid()

    for page in range(0, total_pages_capture):
        logging.warning(f'Crawling page {page}')
        sleep(2)
        pyautogui.press('printscreen')

        item_pixel_x, item_pixel_y = 580, 333
        for item in range(0, 10):
            logging.warning(f'Crawling item {item}')
            pyautogui.moveTo(x=item_pixel_x, y=item_pixel_y, duration=1)
            sleep(1)
            pyautogui.press('printscreen')
            item_pixel_y += 56
        click_next_page()


def run_bot_earrings(total_pages_capture):
    logging.warning('Starting Earrings...')
    click_subcategory_earrings()

    for page in range(0, total_pages_capture):
        logging.warning(f'Crawling page {page}')
        sleep(2)
        pyautogui.press('printscreen')

        item_pixel_x, item_pixel_y = 580, 333
        for item in range(0, 10):
            logging.warning(f'Crawling item {item}')
            pyautogui.moveTo(x=item_pixel_x, y=item_pixel_y, duration=1)
            sleep(1)
            pyautogui.press('printscreen')
            item_pixel_y += 56
        click_next_page()


def run_bot_rings(total_pages_capture):
    logging.warning('Starting Rings...')
    click_subcategory_rings()

    for page in range(0, total_pages_capture):
        logging.warning(f'Crawling page {page}')
        sleep(2)
        pyautogui.press('printscreen')

        item_pixel_x, item_pixel_y = 580, 333
        for item in range(0, 10):
            logging.warning(f'Crawling item {item}')
            pyautogui.moveTo(x=item_pixel_x, y=item_pixel_y, duration=1)
            sleep(1)
            pyautogui.press('printscreen')
            item_pixel_y += 56
        click_next_page()


def run_bot_accessory(total_pages_capture):
    run_bot_necklaces(total_pages_capture=total_pages_capture)
    run_bot_earrings(total_pages_capture=total_pages_capture)
    run_bot_rings(total_pages_capture=total_pages_capture)
