from robocorp.tasks import task
@task
def minimal_task():
    message = "hello"
    message = message + "world!"
# from robocorp.tasks import task
# from robocorp.tasks import get_output_dir
# from RPA.Browser.Selenium import Selenium
# import time, urllib.request, re, sys
# import pandas as pd

# @task
# class NewsScraper:
#     def __init__(self, search_phrase="israels war on gaza", sort_by="date"):
#         self.search_phrase = search_phrase
#         self.sort_by = sort_by

#     def open_browser(self):
#         print("Opening browser...")
#         self.browser = Selenium(auto_close=False) # avoiding auto close after exection is completed

#     def navigate_to_website(self):
#         print("Navigating to news website...")
#         self.browser.open_available_browser('https://www.aljazeera.com/')
#         self.browser.implicit_wait = 30 # implicit wait
#         self.browser.click_element("id:onetrust-accept-btn-handler") # accept cookies
#         time.sleep(2)# explicit wait
#         self.browser.click_element('//*[@id="root"]/div/div[1]/div[1]/div/header/div[4]/div[2]/button')

#     def search_news(self):
#         print("Searching for news...")
#         self.browser.wait_until_element_is_visible("class:search-bar__input")
#         self.browser.input_text("class:search-bar__input", self.search_phrase)# typing search phrase
#         time.sleep(2)# explicit wait
#         self.browser.click_button("Search")
#         self.browser.implicit_wait = 30

#     def sort_news(self):
#         # sorting the new based on date or relevance
#         print("Sorting based on", self.sort_by, "...")
#         self.browser.wait_until_element_is_visible("id:search-sort-option")
#         self.browser.click_element("id:search-sort-option")
#         self.browser.select_from_list_by_value("id:search-sort-option", self.sort_by)
#         time.sleep(15)# explicit wait

#     def scrape_news_details(self):
#         print("Scraping details from website...")
#         #scraping news titles
#         heading_titles = self.browser.find_elements("xpath=//h3[@class='gc__title']")
#         news_titles = [element.text.strip() for element in heading_titles]
#         # scraping new description
#         description_divs = self.browser.find_elements("xpath=//div[@class='gc__body-wrap']")
#         news_descriptions = [element.text for element in description_divs]

#         search_phrase_count = []
#         money_check = []
#         # checking occurance of search phrase in title & description
#         for index in range(len(news_titles)):
#             title = news_titles[index].lower()
#             description = news_descriptions[index].lower()
#             search_phrase_lower = self.search_phrase.lower()
#             occurrences = len(re.findall('(?=('+search_phrase_lower+'))', title)) + \
#                           len(re.findall('(?=('+search_phrase_lower+'))', description))
#             search_phrase_count.append(occurrences)
#             # checkng if money is mentioned in title and description
#             money_found = "$" in title or "usd" in title or "dollar" in title or \
#                           "$" in description or "usd" in description or "dollar" in description
#             money_check.append("True" if money_found else "False")
#         # scraping dates of news
#         date_divs = self.browser.find_elements("xpath=//footer[@class='gc__footer']")
#         news_dates = [element.text for element in date_divs]
#         # scraping images urls of news
#         img_elements = self.browser.find_elements("xpath=//img[@class='article-card__image gc__image']")
#         image_links = [element.get_attribute("src") for element in img_elements]

#         image_filenames = []
#         print("Downloading news images...")
#         for image_link_index, image_link in enumerate(image_links):
#              # removing all punctuations from title
#             image_name = news_titles[image_link_index].replace(" ", "_").replace("|", "_").replace("?", "_").replace("'", "").replace(".", "").replace(":", "").replace(";", "")
#             image_filename = f"output\\{image_name}.jpg"
#             image_filenames.append(image_filename)
#             urllib.request.urlretrieve(image_link, image_filename)
#             time.sleep(2)# explicit wait

#         news_details_dictionary = {
#             "title": news_titles,
#             "date": news_dates,
#             "description": news_descriptions,
#             "picture filename": image_filenames,
#             "search phrase count": search_phrase_count,
#             "money": money_check
#         }
#         return news_details_dictionary

#     def write_to_excel(self, data_dictionary):
#         print("Writing scraped data to Excel file...")
#         df = pd.DataFrame(data_dictionary)
#         excel_file = 'output\\news_scraped_data.xlsx'
#         df.to_excel(excel_file, index=False)
#         print("Completed!")

#     def run_task(self):
#         self.open_browser()
#         self.navigate_to_website()
#         self.search_news()
#         self.sort_news()
#         news_details = self.scrape_news_details()
#         self.write_to_excel(news_details)
#         self.browser.close_browser()

# # Usage
# search_phrase = "israel's war on Gaza"
# sort_by = "date"
# scraper = NewsScraper(search_phrase, sort_by)
# scraper.run_task()