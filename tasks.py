import logging
import re
import time
import urllib.request
#import json

from robocorp.tasks import task
from robocorp import workitems
from RPA.Browser.Selenium import Selenium
from RPA.Excel.Files import Files


class NewsScraper:
    def __init__(self, search_phrase, sort_by):
        self.search_phrase = search_phrase
        self.sort_by = sort_by
        self.browser = Selenium(auto_close=False)
        self.excel = Files()
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.logger.propagate = False  # Disable propagation

        # Add console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

    def scrape_news(self):
        self.logger.info("Opening browser...")
        self.browser.open_available_browser('https://www.aljazeera.com/')
        self.browser.click_element("id:onetrust-accept-btn-handler")  # Accept cookies
        time.sleep(2)
        self.browser.click_element('//*[@id="root"]/div/div[1]/div[1]/div/header/div[4]/div[2]/button')
        self.logger.info("Searching for news...")
        self.browser.wait_until_element_is_visible("class:search-bar__input")
        self.browser.input_text("class:search-bar__input", self.search_phrase)
        time.sleep(2)
        self.browser.click_button("Search")
        self.logger.info("Sorting based on %s ...", self.sort_by)
        self.browser.wait_until_element_is_visible("id:search-sort-option")
        self.browser.click_element("id:search-sort-option")
        self.browser.select_from_list_by_value("id:search-sort-option", self.sort_by)
        time.sleep(15)

        self.logger.info("Scraping details from website...")
        heading_titles = self.browser.find_elements("xpath=//h3[@class='gc__title']")
        news_titles = [element.text.strip() for element in heading_titles]

        description_divs = self.browser.find_elements("xpath=//div[@class='gc__body-wrap']")
        news_descriptions = [element.text for element in description_divs]

        search_phrase_count = []
        money_check = []
        for index in range(len(news_titles)):
            title = news_titles[index].lower()
            description = news_descriptions[index].lower()
            search_phrase_lower = self.search_phrase.lower()
            occurrences = len(re.findall('(?=('+search_phrase_lower+'))', title)) + \
                len(re.findall('(?=('+search_phrase_lower+'))', description))
            search_phrase_count.append(occurrences)
            money_check.append(any(term in title or term in description
                                   for term in ["$", "usd", "dollar"]))

        date_divs = self.browser.find_elements("xpath=//footer[@class='gc__footer']")
        news_dates = [element.text for element in date_divs]

        img_elements = self.browser.find_elements("xpath=//img[@class='article-card__image gc__image']")
        image_links = [element.get_attribute("src") for element in img_elements]

        image_filenames = []
        for image_link_index, image_link in enumerate(image_links):
            image_name = news_titles[image_link_index].replace(" ", "_").replace("|", "_").replace("?", "_") \
                .replace("'", "").replace(".", "").replace(":", "").replace(";", "")
            image_filename = f"output/{image_name}.jpg"
            image_filenames.append(image_filename)
            urllib.request.urlretrieve(image_link, f"output/{image_name}.jpg")
            time.sleep(2)

        new_details_dictionary = {"title": news_titles, "date": news_dates, "description": news_descriptions,
                                  "picture filename": image_filenames, "search phrase count": search_phrase_count,
                                  "money": money_check}

        # Specify the Excel file path
        excel_file = "output/news_scraped_data.xlsx"

        # Create a new Excel file or overwrite if it already exists
        self.excel.create_workbook(excel_file)

        try:
            self.excel.remove_worksheet("Sheet1")
        except Exception:
            pass

        # Write the dictionary to the Excel file
        self.excel.create_worksheet("Sheet1", new_details_dictionary, header=True)

        # Save and close the Excel file
        self.excel.save_workbook()
        self.excel.close_workbook()

        self.logger.info("Completed!")


@task
def minimal_task():
    # Initialize variables
    search_phrase = ""
    sort_by = ""

    # Fetch input parameters from Robocorp Work Item
    for item in workitems.inputs:
        search_phrase = item.payload["search_phrase"]
        sort_by = item.payload["sort_by"]
        print("search_phrase: ",search_phrase)
        print("sort_by: ",sort_by)
        break
    print("search_phrase: ",search_phrase)
    print("sort_by: ",sort_by)
    # Instantiate NewsScraper and scrape news
    scraper = NewsScraper(search_phrase, sort_by)
    scraper.scrape_news()

minimal_task()