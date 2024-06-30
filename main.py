from bs4 import BeautifulSoup
from requests import request
import lxml
from tqdm import tqdm
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import time
import urllib3

# Set up Selenium options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run Chrome in headless mode
chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration

# Set up Chrome driver
driver = webdriver.Chrome(options=chrome_options)

# Define the URL
url = r"https://www.daraz.pk/#hp-flash-sale"

# Load the page using Selenium
driver.get(url)

# Get the page source
time.sleep(3)
page_source = driver.page_source

# Parse the page source with BeautifulSoup
soup = BeautifulSoup(page_source, "lxml")

# Extract the product information
productList = soup.findAll('a', attrs={'class': 'card-fs-content-body-unit hp-mod-card-hover J_FSItemUnit'})

# Create an empty dictionary to store the data
data = {
    'name': [],
    'current price': [],
    'original price': [],
    'link': [],
    'rating' : []
}

# Iterate over the product list and extract the data
for i in tqdm(productList):
    data['name'].append(i.find('div', attrs={'class': 'fs-card-title'}).text)
    data['current price'].append(i.find('div', attrs={'class': 'fs-card-price'}).find('span', class_='price').text)
    data['original price'].append(i.find('div', class_='fs-card-origin-price').find('span', class_='price').text)
    data['link'].append(i['href'])
    data['rating'].append('-')

categories = ['grocers-shop','beauty-health','mens-fashion','womens-fashion','mother-baby','bedding-bath','furniture-decor','kitchen-dining','laundry-cleaning','home-improvement-tools','stationery-craft','books-games-music','phones-tablets','computing','consumer-electronics','camera','home-appliances','sports-travel','jewellery-watches-eyewear','bags-travel']

for c in tqdm(categories):
    url = "https://www.daraz.pk/" + c+ "/?page=1&sort=order"
    driver.get(url)
    time.sleep(3)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "lxml")

    productList = soup.findAll('a', attrs={'class': 'product-card--vHfY9'})
    if len(productList) < 5:
        continue
    for i in tqdm(range(5)):
        item = productList[i].find('div', attrs={'class': 'description--H8JN9'})
        data['name'].append(item.find('div', attrs={'class': 'title-wrapper--IaQ0m'}).text)
        data['current price'].append(item.find('div', attrs={'id': 'id-price'}).find('div', attrs={'class':'price-wrapper--S5vS_'}).find('div',attrs={'class': 'current-price--Jklkc'}).find('span',attrs={'class': 'currency--GVKjl'}).text)
        data['original price'].append(item.find('div', attrs={'id': 'id-price'}).find('div', attrs={'class':'price-wrapper--S5vS_'}).find('div',attrs={'class': 'original-price--lHYOH'}).find('del',attrs={'class': 'currency--GVKjl'}).text)
        data['link'].append(productList[i]['href'])
        data['rating'].append(item.find('div', attrs={'class': 'rating-wrapper--caEhB'}).find('div', attrs={'class': 'rating--ZI3Ol rating--pwPrV'}).find('span', attrs={'class': 'ratig-num--KNake rating--pwPrV'}).text)

driver.quit()
data = pd.DataFrame(data)

#save data to topproducts.csv
data.to_csv('topproducts.csv', index=False)