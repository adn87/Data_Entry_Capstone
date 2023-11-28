from bs4 import BeautifulSoup
import requests
from os import environ
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

chromeOptions = webdriver.ChromeOptions()
chromeOptions.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chromeOptions)

# Scrape the links, addresses, and prices of the rental properties
header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/84.0.4147.125 Safari/537.36",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
}
FORM = environ.get("FORM")

# Use our Zillow-Clone website (instead of Zillow.com)
response = requests.get("https://appbrewery.github.io/Zillow-Clone/", headers=header)
data = response.text

soup = BeautifulSoup(data, "html.parser")

# Create a list of all the links on the page using a CSS Selector
all_link_elements = soup.select(".StyledPropertyCardDataWrapper a")
all_links = [link["href"] for link in all_link_elements]
print(f"There are {len(all_links)} links to individual listings in total: \n")
print(all_links)

# Create a list of all the prices on the page using a CSS Selector
# Get a clean dollar price and strip off any "+" symbols and "per month" /mo abbreviation
all_prices_elements = soup.select(".StyledPropertyCardDataArea-fDSTNn div span")
all_prices = [price.get_text().replace("/mo", "").split("+")[0] for price in all_prices_elements if "$" in price.text]
print(f"\n After having been cleaned up, the {len(all_prices)} prices now look like this: \n")
print(all_prices)

# Create a list of all the addresses on the page using a CSS Selector
all_addresses_elements = soup.select(".StyledPropertyCardDataWrapper address")
all_addresses = [address.get_text().replace(" | ", " ").strip() for address in all_addresses_elements]
print(f"\n After having been cleaned up, the {len(all_addresses)} addresses now look like this: \n")
print(all_addresses)

# Get the Google sheet
# Add fill in the link to your own Google From
for n in range(len(all_links)):
    driver.get(FORM)
    time.sleep(2)

    # Use the xpath to select the "short answer" fields in Google Form.
    address = driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div['
                                                  '1]/div/div[1]/input')
    price = driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div['
                                                '1]/div/div[1]/input')
    link = driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div['
                                               '1]/div/div[1]/input')
    submit_button = driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div['
                                                        '1]/div/span/span')

    address.send_keys(all_addresses[n])
    price.send_keys(all_prices[n])
    link.send_keys(all_links[n])
    submit_button.click()
