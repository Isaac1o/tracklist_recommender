from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup
import time


site_url = 'https://www.1001tracklists.com/genre/dubstep/index.html'


def create_driver(chromedriver_path) -> webdriver.Chrome:
    # Create webdriver that will be used to open Chrome.
    # Link to fix permission error for chromedriver
    # https://stackoverflow.com/questions/60362018/macos-catalinav-10-15-3-error-chromedriver-cannot-be-opened-because-the-de
    return webdriver.Chrome(executable_path=chromedriver_path)


def wait_for_footer(wait_driver):
    try:
        element = wait_driver.until(EC.presence_of_element_located((By.ID, 'footer')))
    except Exception as e:
        print(e)
        return False
    return True


def check_captcha(driver, wait_driver):
    try:
        captcha_element = driver.find_element(By.ID, 'iScrollCaptcha')
    except Exception as e:
        captcha_element = None

    if captcha_element:
        try:
            print('Captcha Found!!!')
            wait_driver.until(EC.staleness_of(captcha_element))
        except Exception as e:
            print(e)
            print('Did not solve captcha in time')
            return False

    return True


def count_num_tracklists_present(driver) -> int:
    # Count the number of links loaded on the page
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    return len(soup.find_all(class_='bTitle'))


def scroll_to_bottom(driver, find_n_links=1000, seconds_wait=20):
    # Scrolls until loading takes too long, blocked by CAPTCHA, or desired number of links found
    wait_driver = WebDriverWait(driver, timeout=seconds_wait)
    cur_num_links = 0
    i = 1

    print('Scrolling...')
    while True:
        # TODO figure out how to kill the loop when at the bottom of the page
        # TODO Try killing the loop if the number of links remain the same for n iterations
        driver.execute_script(f'window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(.5)

        if check_captcha(driver=driver, wait_driver=wait_driver) is False:
            break

        if i % 50 == 0:
            num_links = count_num_tracklists_present(driver)
            print(f'{i}: {num_links} links')
            if num_links >= find_n_links:
                print(f'Desired number of links found: {num_links}')
                break
            if num_links == cur_num_links:
                print('No longer loading content')
                break
            cur_num_links = num_links
        i += 1

    print('Scrolling complete')


def parse_tracklist_urls(driver) -> list:
    # Get all the tracklist urls and append them to a list.
    BASE_URL = 'https://www.1001tracklists.com'
    urls = []
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    for parent in soup.find_all(class_='bTitle'):
        link = parent.find('a').attrs['href']
        urls.append(f'{BASE_URL}{link}')

    return urls
