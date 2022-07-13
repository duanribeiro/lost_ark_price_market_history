import pyautogui
from time import sleep
import logging

logging.basicConfig(format='[%(asctime)s] %(message)s')


def click_category_acessory():
    logging.warning('Clicking on acessory')
    pyautogui.moveTo(x=240, y=286, duration=1)
    pyautogui.click(x=240, y=286, duration=1)
    sleep(2)


def click_subcategory_neklaces():
    logging.warning('Clicking on neklace')
    pyautogui.moveTo(x=240, y=343, duration=1)
    pyautogui.click(x=240, y=343, duration=1)
    sleep(5)


def click_subcategory_earrings():
    logging.warning('Clicking on earrings')
    pyautogui.moveTo(x=240, y=372, duration=1)
    pyautogui.click(x=240, y=372, duration=1)
    sleep(5)


def click_subcategory_rings():
    logging.warning('Clicking on rings')
    pyautogui.moveTo(x=240, y=399, duration=1)
    pyautogui.click(x=240, y=399, duration=1)
    sleep(5)


def click_order_desc_bid():
    logging.warning('Clicking on ordering descending bid')
    pyautogui.moveTo(x=980, y=203, duration=1)
    pyautogui.click(x=980, y=203, duration=1)
    sleep(2)


def click_next_page():
    logging.warning('Clicking on next page')
    pyautogui.moveTo(x=815, y=639, duration=1)
    pyautogui.click(x=815, y=639, duration=1)
    sleep(5)


def run_bot_nekclaces(TOTAL_PAGES_CAPTURE):
    logging.warning('Starting Necklaces...')
    sleep(5)
    click_category_acessory()
    click_subcategory_neklaces()
    click_order_desc_bid()

    for page in range(0, TOTAL_PAGES_CAPTURE):
        logging.warning(f'Crawling page {page}')
        sleep(5)
        pyautogui.press('printscreen')

        item_pixel_x, item_pixel_y = 411, 240
        for item in range(0, 10):
            logging.warning(f'Crawling item {item}')
            pyautogui.moveTo(x=item_pixel_x, y=item_pixel_y, duration=1)
            sleep(2)
            pyautogui.press('printscreen')
            item_pixel_y += 40
        click_next_page()


def run_bot_earrings(TOTAL_PAGES_CAPTURE):
    logging.warning('Starting Earrings...')
    click_subcategory_earrings()

    for page in range(0, TOTAL_PAGES_CAPTURE):
        logging.warning(f'Crawling page {page}')
        sleep(5)
        pyautogui.press('printscreen')

        item_pixel_x, item_pixel_y = 411, 240
        for item in range(0, 10):
            logging.warning(f'Crawling item {item}')
            pyautogui.moveTo(x=item_pixel_x, y=item_pixel_y, duration=1)
            pyautogui.press('printscreen')
            sleep(2)
            item_pixel_y += 40
        click_next_page()


def run_bot_rings(TOTAL_PAGES_CAPTURE):
    logging.warning('Starting Rings...')
    click_subcategory_rings()

    for page in range(0, TOTAL_PAGES_CAPTURE):
        logging.warning(f'Crawling page {page}')
        sleep(5)
        pyautogui.press('printscreen')

        item_pixel_x, item_pixel_y = 411, 240
        for item in range(0, 10):
            logging.warning(f'Crawling item {item}')
            pyautogui.moveTo(x=item_pixel_x, y=item_pixel_y, duration=1)
            pyautogui.press('printscreen')
            sleep(2)
            item_pixel_y += 40
        click_next_page()


def run_bot_acessory(TOTAL_PAGES_CAPTURE):
    run_bot_nekclaces(TOTAL_PAGES_CAPTURE=TOTAL_PAGES_CAPTURE)
    run_bot_earrings(TOTAL_PAGES_CAPTURE=TOTAL_PAGES_CAPTURE)
    run_bot_rings(TOTAL_PAGES_CAPTURE=TOTAL_PAGES_CAPTURE)
