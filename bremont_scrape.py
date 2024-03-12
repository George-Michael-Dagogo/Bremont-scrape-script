

from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent
#from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.service import Service
import time
import requests  # For making HTTP requests
from bs4 import BeautifulSoup  # For parsing HTML content
from fake_useragent import UserAgent  # For generating random user agents
import pandas as pd  # For data manipulation and creating DataFrames
import numpy as np


service = Service(executable_path=r'C:\Users\H i - G E O R G E\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe')
options = Options()
ua = UserAgent()
userAgent = ua.random
options.add_argument(f'user-agent={userAgent}')
options.add_experimental_option("prefs", {"profile.default_content_settings.cookies": 2})
options.add_argument('--blink-settings=imagesEnabled=false')
options.add_argument("--disable-popup-blocking")
options.add_argument("--no-sandbox")
#options.add_argument("--window-size=1920,1080")


driver = webdriver.Chrome(service=service,options=options)


driver.get("https://www.bremont.com/collections/mens-watches")

WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="cookiescript_accept"]'))).click()

time.sleep(20)


while True:
    try:
      element = driver.find_element(By.CLASS_NAME,'btn-Button.btn-Button-tertiary.boost-pfs-filter-load-more-button')
      WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME,'btn-Button.btn-Button-tertiary.boost-pfs-filter-load-more-button')))
      driver.execute_script("arguments[0].scrollIntoView();", element)
      driver.execute_script("arguments[0].click();", element)
      time.sleep(10)
    except Exception as e:
        print(e)
        break
    print("Complete")
    time.sleep(10)



# Initialize empty lists to store scraped data
watch_URL = []
reference_numbers = []
brands = []
nick_names = []
marketing_names = []
currencies = []
image_urls = []
parent_models = []
case_materials = []
case_backs = []
crystals = []
water_resistances = []
weights = []
dial_colours = []
numerals = []
bracelet_materials = []
bracelet_colors = []
clasp_types = []
movements = []
calibers = []
power_reserves = []
frequencies = []
jewels = []
functional = []
description = []
short_description = []


page = driver.page_source

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(page, "html.parser")

# Find all elements with class "prd-Card prd-Card-grid util-FauxLink"
# These likely represent individual watch listings
watch_box = soup.find_all('div', class_= "prd-Card prd-Card-grid util-FauxLink")

# Loop through each watch listing
for box in watch_box:

    # Extract the watch URL (if it exists)
    if box.find('a', attrs={"href": True}) is not None:
        link = box.find('a', attrs={"href": True})
        link = link['href']
        watch_URL.append('https://www.bremont.com/' + link)
        # Extract reference number from the URL (assuming a specific format)
        reference_numbers.append(link.replace('/products/', ''))
    else:
        watch_URL.append('None')
        reference_numbers.append('None')  # Indicate missing data

    # Extract the brand name (if it exists)
    if box.find('h3', class_="prd-Card_Title fz-12_20") is not None:
        brand = box.find('h3', class_="prd-Card_Title fz-12_20").text
        brands.append(brand)
    else:
        brands.append('None')  # Indicate missing data

    # Extract the nickname (if it exists)
    if box.find('li', class_="prd-Card_SpecItem") is not None:
        nick_name = box.find('li', class_="prd-Card_SpecItem").text
        # Replace "case Size" with "None" (case-insensitive)
        # Check for exact phrase to avoid unintended replacements
        if "case size" in nick_name.lower():
            nick_name = "None"
        nick_names.append(nick_name)
    else:
        nick_names.append('None')  # Indicate missing data

    # Extract the marketing name (if it exists)
    if box.find('p', class_="prd-Card_Kicker fz-12_16") is not None:
        marketing_name = box.find('p', class_="prd-Card_Kicker fz-12_16").text
        marketing_names.append(marketing_name)
    else:
        marketing_names.append('None')  # Indicate missing data

    # Extract the currency and price (if it exists)
    if box.find('dd', class_="prd-Price_Dd prd-Price_Dd-last") is not None:
        currency = box.find('dd', class_="prd-Price_Dd prd-Price_Dd-last").text.replace('\n', '').strip()
        if '£' in currency:
            # Assuming price follows a specific format, replace symbols
            # and potentially separate currency and price (modify if needed)
            currencies.append(currency.replace('£', 'EUR ').replace('$', 'USD '))
        else:
            currencies.append('None')  # Indicate missing data
    else:
        currencies.append('None')  # Indicate missing data

    # Extract the image URL (if it exists)
    if box.find('img', attrs={"src": True}) is not None:
        image_url = box.find('img', attrs={"src": True})
        image_url = image_url['src']
        image_urls.append(image_url.replace('//',''))
    else:
      image_urls.append('None')


short_desc_1 = 'In stock. Free express delivery within 2 - 4 working days (UK only). International orders will take longer.'
short_desc_2 = 'Hand built to order. Estimated dispatch in 2 - 4 weeks. We will contact you directly if for any reason delivery may take longer.'

def get_parent_models(url):
    # Create a UserAgent object for a random user agent
    ua = UserAgent()
    userAgent = ua.random
    headers = {'User-Agent': userAgent}

    # Send a request to the given URL
    page = requests.get(url, headers=headers)

    # Parse the HTML content
    soup = BeautifulSoup(page.content, "html.parser")
    try:
        # Find the breadcrumb trail element, handling potential NoneType
        parent_model_element = soup.find('ul', class_="bdc-Breadcrumb_Items").text
        if parent_model_element:
            parent_model = parent_model_element
            # Clean up the text for better formatting
            parent_model = parent_model.replace('Home', ' ').replace('\n', ' ').strip().replace('   ', ' > ')
            print(parent_model)
        else:
            parent_model = 'None'

        # Append the extracted (or None) parent model to the list
        parent_models.append(parent_model)

    except AttributeError as E:
        parent_models.append('None')  # Append 'None' if any other AttributeError occur





    describe = soup.find('div', class_="prd-Description_Content").text
    # Clean up the text for better formatting
    describe = describe.replace('Description', '').replace('\n', '').strip()
    # Append the extracted parent model to the global list
    description.append(describe)

    short_describe = soup.find('div', class_="prd-Product_ShortDesc fz-14_24 rte-RichText").text
    # Clean up the text for better formatting
    short_describe  = short_describe.replace('\n', '').replace(short_desc_1,'').replace(short_desc_2,'').strip()
    # Append the extracted parent model to the global list
    short_description.append(short_describe)

    product_body = soup.find('div', attrs={"class": 'prd-TechSpec_Content'})
    product_bodies = product_body.find_all('li', attrs={"class": 'prd-Accordion_Item'})
    # Check if there are at least two elements
    if len(product_bodies) >= 8:
        movement = product_bodies[0].text.replace('\n','').replace('Movement','').strip()
        movements.append(movement)
        calibers.append(movement)
        jewels.append(movement)
        frequencies.append(movement)
        power_reserves.append(movement)

        functioning = product_bodies[1].text.replace('\n','').replace('Functions','').strip()
        functional.append(functioning)

        case_material = product_bodies[2].text.replace('\n','').replace('Case','').strip()
        case_materials.append(case_material)

        case_back = product_bodies[3].text.replace('\n','').replace('Case back','').replace('Case Back','').strip()
        case_backs.append(case_back)

        crystal = product_bodies[5].text.strip()
        crystals.append(crystal)

        water_resistance = product_bodies[6].text.replace('Water Resistance','').replace('\n','').strip()
        water_resistances.append(water_resistance)

        weight = product_bodies[-1].text.strip()
        weights.append(weight)

        dial_colour = product_bodies[4].text.replace('Dial & Hands','').replace('\n','').strip()
        dial_colours.append(dial_colour)
        numerals.append(dial_colour)
        bracelet_material  = product_bodies[-3].text.strip().replace('\n','')
        bracelet_materials.append(bracelet_material)
        bracelet_colors.append(bracelet_material)
        clasp_types.append(bracelet_material)
    elif len(product_bodies) >= 10:
        movement = product_bodies[0].text.replace('\n','').replace('Movement','').strip()
        movements.append(movement)
        calibers.append(movement)
        jewels.append(movement)
        frequencies.append(movement)
        power_reserves.append(movement)

        functioning = product_bodies[1].text.replace('\n','').replace('Functions','').strip()
        functional.append(functioning)

        case_material = product_bodies[2].text.replace('\n','').replace('Case','').strip()
        case_materials.append(case_material)

        case_back = product_bodies[3].text.replace('\n','').replace('Case back','').replace('Case Back','').strip()
        case_backs.append(case_back)

        crystal = product_bodies[5].text.strip()
        crystals.append(crystal)

        water_resistance = product_bodies[6].text.replace('Water Resistance','').replace('\n','').strip()
        water_resistances.append(water_resistance)

        weight = product_bodies[-1].text.strip()
        weights.append(weight)
        dial_colour = product_bodies[4].text.replace('Dial & Hands','').replace('\n','').strip()
        dial_colours.append(dial_colour)
        numerals.append(dial_colour)


        bracelet_material  = product_bodies[-3].text.strip().replace('\n','')
        bracelet_materials.append(bracelet_material)
        bracelet_colors.append(bracelet_material)
        clasp_types.append(bracelet_material)


    else:
        # No second element found, append 'None'
        case_materials.append('None')
        case_backs.append('None')
        crystals.append('None')
        weights.append('None')
        bracelet_materials.append('None')
        bracelet_colors.append('None')
        clasp_types.append('None')
        water_resistances.append('None')
        movements.append('None')
        calibers.append('None')
        jewels.append('None')
        frequencies.append('None')
        power_reserves.append('None')
        dial_colours.append('None')
        numerals.append('None')



for i in watch_URL:
    # Call the function for each extracted watch URL
    get_parent_models(i)
    print(i)  # Print the current URL (likely for debugging purposes)

# Create a DataFrame using the collected data
bremont_watch_df = pd.DataFrame({
    'reference_number': reference_numbers,
    'watch_URL': watch_URL,
    'brands': brands,
    'nick_names': nick_names,
    'marketing_name': marketing_names,
    'currency': currencies,
    'image_url': image_urls,
    'parent_models': parent_models,
    'case_material': case_materials,
    'case_back':case_backs,
    'crystal':crystals,
    'water_resistance': water_resistances,
    'weight': weights,
    'dial_colour': dial_colours,
    'numeral': numerals,
    'bracelet_material': bracelet_materials,
    'clasp_type': clasp_types,
    'bracelet_color': bracelet_colors,
    'movement' : movements,
     'caliber' : calibers,
    'power_reserve': power_reserves,
    'frequency': frequencies,
    'jewel': jewels,
    'features':functional,
    'description': description,
    'short_description' : short_description



})


bremont_watch_df[['currency', 'price']] = bremont_watch_df['currency'].str.split(' ',n = 1, expand=True)

# Optionally convert the price column to numeric (assuming it's numeric)
bremont_watch_df['price'] = pd.to_numeric(bremont_watch_df['price'].str.replace(',', ''), errors='coerce')  # Handle non-numeric values

def get_case_diameter(text):
  diameter_str = text.split("Diameter: ")[-1].split(" ")[0]
  diameter_str = diameter_str.replace('Case','').replace('Central','None')
  try:
    return diameter_str
  except ValueError:
    return 'None'


def get_case_length(text):
  diameter_str = text.split("Length: ")[-1].split(" ")[0]
  diameter_str = diameter_str.replace('Case','').replace('Central','None')
  try:
    return diameter_str
  except ValueError:
    return 'None'


def get_case_depth(text):
  diameter_str = text.split("Depth: ")[-1].split(" ")[0]
  diameter_str = diameter_str.replace('Lug','').replace('Stainless','None')
  try:
    return diameter_str
  except ValueError:
    return 'None'


bremont_watch_df[['Type', 'style' , 'year_introduced', 'specific model','case_shape','case_finish','bezel_material', 'bezel_color']] = ''
# Apply the function to the 'text' column and add the result as a new column
bremont_watch_df['case_diameter'] = bremont_watch_df['case_material'].apply(get_case_diameter)

bremont_watch_df['lug_to_lug'] = bremont_watch_df['case_material'].apply(get_case_length)

bremont_watch_df['case_thickness'] = bremont_watch_df['case_material'].apply(get_case_depth)

bremont_watch_df['between_lugs'] = bremont_watch_df['case_material']
l=['sapphire crystal', 'fiber glass', 'mineral glass']
s='|'.join(l)

bremont_watch_df['crystal']=bremont_watch_df['crystal'].str.findall(s)
bremont_watch_df['crystal']=np.where(bremont_watch_df['crystal'].str.match(s),bremont_watch_df['crystal'],'None')

bremont_watch_df['made_in'] = 'United Kingdom'

bremont_watch_df['brands'] = 'Bremont'

bremont_watch_df

#belmont_watch_df.to_csv('brand.csv')

