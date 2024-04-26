from robocorp.tasks import task
from RPA.Browser.Selenium import Selenium
from RPA.Excel.Files import Files
import time
import urllib.request
import re
import json

class NewsScraper:
    def __init__(self, search_phrase, sort_by):
        self.search_phrase = search_phrase
        self.sort_by = sort_by
        self.browser = Selenium(auto_close=False)
        self.excel = Files()

    def scrape_news(self):
        print("Opening browser...")
        self.browser.open_available_browser('https://www.aljazeera.com/')
        self.browser.click_element("id:onetrust-accept-btn-handler") # Accept cookies
        time.sleep(2)
        self.browser.click_element('//*[@id="root"]/div/div[1]/div[1]/div/header/div[4]/div[2]/button')
        print("Searching for news...")
        self.browser.wait_until_element_is_visible("class:search-bar__input")
        self.browser.input_text("class:search-bar__input", self.search_phrase)
        time.sleep(2)
        self.browser.click_button("Search")
        print("Sorting based on", self.sort_by, "...")
        self.browser.wait_until_element_is_visible("id:search-sort-option")
        self.browser.click_element("id:search-sort-option")
        self.browser.select_from_list_by_value("id:search-sort-option", self.sort_by)
        time.sleep(15)

        print("Scraping details from website...")
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
            occurrences = len(re.findall('(?=('+search_phrase_lower+'))', title)) + len(re.findall('(?=('+search_phrase_lower+'))', description))
            search_phrase_count.append(occurrences)
            money_check.append(any(term in title or term in description for term in ["$", "usd", "dollar"]))

        date_divs = self.browser.find_elements("xpath=//footer[@class='gc__footer']")
        news_dates = [element.text for element in date_divs]

        img_elements = self.browser.find_elements("xpath=//img[@class='article-card__image gc__image']")
        image_links = [element.get_attribute("src") for element in img_elements]

        image_filenames = []
        for image_link_index, image_link in enumerate(image_links):
            image_name = news_titles[image_link_index].replace(" ", "_").replace("|", "_").replace("?", "_").replace("'", "").replace(".", "").replace(":", "").replace(";", "")
            image_filename = f"output/{image_name}.jpg"
            image_filenames.append(image_filename)
            urllib.request.urlretrieve(image_link, f"downloads\\{image_name}.jpg")
            time.sleep(2)

        new_details_dictionary = {"title": news_titles, "date": news_dates, "description": news_descriptions,
                                  "picture filename": image_filenames, "search phrase count": search_phrase_count,
                                  "money": money_check}

        excel_file = "output/news_scraped_data.xlsx"
        self.excel.create_workbook(excel_file)
        self.excel.open_workbook(excel_file)
        for key, values in new_details_dictionary.items():
            worksheet_name = key
            counter = 1
            while worksheet_name in self.excel.sheetnames:
                worksheet_name = f"{key}_{counter}"
                counter += 1
            self.excel.create_worksheet(worksheet_name)
            self.excel.set_cell_value(1, 1, key)
            for index, value in enumerate(values, start=2):
                self.excel.set_cell_value(index, 1, value)
        self.excel.save_workbook()
        self.excel.close_workbook()
        print("Completed!")

@task
def minimal_task():
    # Read input data from file
    with open('configuration.json', 'r') as file:
        input_data = json.load(file)

    # Access variables from input data
    search_phrase = input_data['search_phrase']
    sort_by = input_data['sort_by']

    # Instantiate NewsScraper and scrape news
    scraper = NewsScraper(search_phrase, sort_by)
    scraper.scrape_news()

minimal_task()