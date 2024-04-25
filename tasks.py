from robocorp.tasks import task
from robocorp.tasks import get_output_dir
from RPA.Browser.Selenium import Selenium
import time, urllib.request, re, sys
import pandas as pd

@task
def minimal_task(search_phrase="israels war on gaza",sort_by="date"):
    print("search phrase: ", search_phrase)
    print("sort by: ", sort_by)
    print("opening browser...")
    browser = Selenium(auto_close = False)
    print("navigating to news website...")
    browser.open_available_browser('https://www.aljazeera.com/')
    browser.implicit_wait = 30 # implicit wait for web to get fully loaded
    browser.click_element("id:onetrust-accept-btn-handler") # accept cookies
    time.sleep(2)
    browser.click_element('//*[@id="root"]/div/div[1]/div[1]/div/header/div[4]/div[2]/button')
    # Wait for the search input element to be visible
    print("searching for news...")
    browser.wait_until_element_is_visible("class:search-bar__input")
    browser.input_text("class:search-bar__input", search_phrase)
    time.sleep(2)
    browser.click_button("Search")
    browser.implicit_wait = 30 # implicit wait for web to get fully loaded

    # selecting news filter
    print("sorting based on ", sort_by, " ...")
    browser.wait_until_element_is_visible("id:search-sort-option")
    browser.click_element("id:search-sort-option")
    browser.select_from_list_by_value("id:search-sort-option", sort_by) # fetch results sorted by date or relevance
    time.sleep(15)
    
    print("scraping details from website...")
    # Get the titles of all news search results
    print("scraping titles...")
    heading_titles = browser.find_elements("xpath=//h3[@class='gc__title']")
    news_titles = [element.text.strip() for element in heading_titles]

    # Get the descriptions of all news search results
    print("scraping description...")
    description_divs = browser.find_elements("xpath=//div[@class='gc__body-wrap']")
    news_descriptions = [element.text for element in description_divs]

    # counting search phrase occurance  and checking money in title/description
    print("counting occurance of search phrase in title & description...")
    search_phrase_count = []
    money_check = []
    for index in range(len(news_titles)):
        # converting title, description and phrase to lower case
        title = news_titles[index].lower()
        description = news_descriptions[index].lower()
        search_phrase_lower = search_phrase.lower()
        occurrences = 0

        # counting search phrase occurances in title
        occurrences += len(re.findall('(?=('+search_phrase_lower+'))', title))

        # counting search phrase occurances in description
        occurrences += len(re.findall('(?=('+search_phrase_lower+'))', description))
        search_phrase_count.append(occurrences)
        
        # checking if money found
        if "$" in title or "usd" in title or "dollar" in title or "$" in description or "usd" in description or "dollar" in description:
            money_check.append("True")
        else:
            money_check.append("False")

    # Get the dates of all news search results
    print("scraping dates...")
    date_divs = browser.find_elements("xpath=//footer[@class='gc__footer']")
    news_dates = [element.text for element in date_divs]

    # Get image source of all news search results
    img_elements = browser.find_elements("xpath=//img[@class='article-card__image gc__image']")
    image_links = [element.get_attribute("src") for element in img_elements]
    # downloading all news images from links
    print("downloading news images...")
    image_filnames = []
    for image_link_index in range(len(image_links)):
        image_name = news_titles[image_link_index].replace(" ", "_").replace("|", "_").replace("?", "_").replace("'", "").replace(".", "").replace(":", "").replace(";", "") # removing all punctuations from title
        image_filnames.append("output\\"+image_name+".jpg")
        urllib.request.urlretrieve(image_links[image_link_index], "downloads\\"+image_name+".jpg")
        time.sleep(2)

    # dictionary for news details
    new_details_dictionary = {"title":news_titles, "date":news_dates, "description":news_descriptions, "picture filename":image_filnames, "search phrase count":search_phrase_count, "money":money_check}
    # write dictionary to excel file
    print("writing scraped data to excel file...")
    # Convert dictionary to DataFrame
    df = pd.DataFrame(new_details_dictionary)
    # Write DataFrame to Excel file
    excel_file = 'output\\news_scraped_data.xlsx'
    df.to_excel(excel_file, index=False)
    print("Completed!")
    

# search_phrase = "israel's war on Gaza" # search phrase to search on website
# sort_by = "date" # for date results send parameter 'date' | for relevancy type 'relevance'
#minimal_task(search_phrase, sort_by) # task functiona call