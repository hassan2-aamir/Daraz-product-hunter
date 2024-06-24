'''import urllib3
from bs4 import BeautifulSoup
from requests import request
import lxml
from tqdm import tqdm

year=input("Enter the year: ")

url = "http://www.imdb.com/search/title?release_date=" + year + ',' + year + '&title_type=feature'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
ourUrl = urllib3.PoolManager().request('GET', url,headers=headers).data
soup = BeautifulSoup(ourUrl, "lxml")


movieList = soup.findAll('div', attrs={'class': 'sc-b189961a-0 hBZnfJ'})
print(len(movieList))
for div_item in tqdm(movieList):
    div = div_item.find('div',attrs={'class':'ipc-title ipc-title--base ipc-title--title ipc-title-link-no-icon ipc-title--on-textPrimary sc-b189961a-9 iALATN dli-title'})
    header = div.findChildren('a',attrs={'class':'ipc-title-link-wrapper'})
    print ('Movie: ' + str((header[0].findChildren('h3'))[0].contents[0].encode('utf-8').decode('ascii', 'ignore')))'''

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

# Set up Selenium options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run Chrome in headless mode
chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration

# Set up Chrome driver
driver_path = r'C:\Users\hp\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\LocalCache\local-packages\Python311\site-packages\chromedriver_win32\chromedriver.exe' # Replace with your actual path to chromedriver
driver = webdriver.Chrome(options=chrome_options)

# Define the URL
url = r"https://www.daraz.pk/#hp-flash-sale"

# Load the page using Selenium
driver.get(url)

# Get the page source
time.sleep(3)
page_source = driver.page_source

# Close the driver
driver.quit()

# Parse the page source with BeautifulSoup
soup = BeautifulSoup(page_source, "lxml")

# Extract the product information
productList = soup.findAll('a', attrs={'class': 'card-fs-content-body-unit hp-mod-card-hover J_FSItemUnit'})

# Create an empty dictionary to store the data
data = {
    'name': [],
    'current price': [],
    'original price': [],
    'discount': [],
    'link': []
}

# Iterate over the product list and extract the data
for i in productList:
    data['name'].append(i.find('div', attrs={'class': 'fs-card-title'}).text)
    data['current price'].append(i.find('div', attrs={'class': 'fs-card-price'}).find('span', class_='price').text)
    data['original price'].append(i.find('div', class_='fs-card-origin-price').find('span', class_='price').text)
    data['discount'].append(i.find('span', class_='fs-discount').text.strip())
    data['link'].append(i['href'])

# Create a DataFrame from the data dictionary
data = pd.DataFrame(data)

# Print the DataFrame
print(data)

