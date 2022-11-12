from src.dataset.web_scraper import *
import time
import argparse


if __name__ == '__main__':

    parser = argparse.ArgumentParser(usage='Parse tracklist urls from 1001.tracklists.com')
    parser.add_argument('--genre', '-g', type=str, help='Genre to parse',
                        choices=['dubstep', 'trap', 'house'], required=True)
    parser.add_argument('--chromedriver_path', '-c', type=str, help='Path to Chromedriver', required=True)
    parser.add_argument('--save_dir', '-s', help='Path to save the url text file', required=True)
    args = parser.parse_args()
    genre = args.genre
    chromedriver_path = args.chromedriver_path
    dir = args.save_dir

    # Start and load website
    print('Opening Chrome')
    driver = create_driver(chromedriver_path=chromedriver_path)
    driver.get(f'https://www.1001tracklists.com/genre/{genre}/index.html')
    time.sleep(5)

    # Scroll as far as possible and extract all urls
    scroll_to_bottom(driver=driver, find_n_links=5_000, seconds_wait=120)
    urls = parse_tracklist_urls(driver=driver)
    urls_string = '\n'.join(urls)

    # Save urls to a file
    print('Saving...')
    with open(f'{dir}/{genre}_tracklist_urls.txt', 'w') as f:
        f.write(urls_string)
        print('Successfully saved to file!')

    driver.quit()
