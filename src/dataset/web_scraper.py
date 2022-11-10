from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup
import time


chromedriver_path = 'chromedriver/chromedriverv107'
site_url = 'https://www.1001tracklists.com/genre/dubstep/index.html'


def create_driver(chromedriver_path) -> webdriver.Chrome:
    # Create webdriver that will be used to open Chrome.
    # Link to fix permission error for chromedriver
    # https://stackoverflow.com/questions/60362018/macos-catalinav-10-15-3-error-chromedriver-cannot-be-opened-because-the-de
    return webdriver.Chrome(executable_path=chromedriver_path)


def wait_for_footer(wait_driver):
    try:
        element = wait_driver.until(EC.presence_of_element_located((By.ID, 'footer')))
    except TimeoutError:
        print('Loading TimeoutError')
        return False
    return True


def count_num_tracklists_present(driver) -> int:
    # Count the number of links loaded on the page
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    return len(soup.find_all(class_='bTitle'))


def scroll_to_bottom(driver, find_n_links=1000):
    # Scrolls until loading takes too long, blocked by CAPTCHA, or desired number of links found
    wait_driver = WebDriverWait(driver, timeout=20)  #TODO increase timeout to give time to fill in CAPTCHA
    scroll_height = driver.execute_script('return document.body.scrollHeight;')
    i = 1

    while True:
        driver.execute_script(f'window.scrollTo(0, {scroll_height});')
        new_scroll_height = driver.execute_script('return document.body.scrollHeight;')
        page_bottom_present = wait_for_footer(wait_driver=wait_driver)
        # Break condition:
        if not page_bottom_present:
            break
        if i % 50 == 0:
            num_links = count_num_tracklists_present(driver)
            if num_links >= find_n_links:
                print(f'Desired number of links found: {num_links}')
                break
        i += 1

        scroll_height = new_scroll_height


def extract_tracklist_urls():
    # TODO compatability for all genres
    # Get the urls of the tracklists and save them to a text file.
    driver = create_driver(chromedriver_path)
    driver.get('https://www.1001tracklists.com/genre/dubstep/index.html')
    time.sleep(20)

    # Scroll as far as possible
    scroll_to_bottom(driver=driver)

    # TODO: Use bs4 to get all the links and save them in a file

    # # Locate container that has all the tracklist links
    # middle_container = driver.find_element(By.ID, 'middle')
    #
    # tracklist_containers = middle_container.find_elements(By.CLASS_NAME, 'bTitle')
    # for tracklist_container in tracklist_containers:
    #     print(tracklist_container.find_element(By.TAG_NAME, 'a').get_attribute('href'))


    print('sleeping until quitting')
    time.sleep(10)
    driver.quit()


if __name__ == '__main__':
    extract_tracklist_urls()