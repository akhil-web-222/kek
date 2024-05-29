import streamlit as st
import csv
from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime
from bs4 import BeautifulSoup
import pandas as pd
driver = None
#service = Service(executable_path='/Users/admin/Desktop/Samsung Prism/chromedriver')

def flipkart_scraper(query,max_size):

    products = {}

    # Open Flipkart website
    driver.get('https://www.flipkart.com')

    # Maximize window
    driver.maximize_window()

    # Find search input and search button, then search for the query
    input_search = driver.find_element(By.XPATH, '//input[@class="Pke_EE"]')
    search_button = driver.find_element(By.XPATH, '//button[@class="_2iLD__"]')
    input_search.send_keys(query)
    search_button.click()

    # Wait for Mobiles category link to be clickable and click on it
    mobiles_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//a[@title="Mobiles"]')))
    mobiles_button.click()

    # Wait for product links to appear
    WebDriverWait(driver, 10).until(EC.visibility_of_any_elements_located((By.XPATH , '//a[@class="CGtC98"]')))

    # Parse the first page
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    Block = soup.find("div", class_="DOjaWF gdgoEp")
    product_links = Block.find_all("a", class_="CGtC98") 

    # Counter variable
    i=0

    # Parse each product
    for product_link in product_links:
        if i<max_size:
            product_url = "https://www.flipkart.com" + product_link.get("href")
            try:
                driver.get(product_url)
                sleep(2)

                details = {}

                # Get product image URL
                image_url_element = driver.find_element(By.XPATH, "//img[@class='DByuf4 IZexXJ jLEJ7H']")
                image_url = image_url_element.get_attribute("src")
                details["image_url"] = image_url if image_url else "Image not available"

                # Get product name
                product_name_element = driver.find_element(By.XPATH, "//span[@class='VU-ZEz']")
                product_name = product_name_element.text
                details["name"] = product_name if product_name else "Name not available"

                # Get product price
                try:
                    product_price_element = driver.find_element(By.XPATH, "//div[@class='Nx9bqj CxhGGd']")
                    product_price = product_price_element.text
                    details["price"] = product_price if product_price else "Price not available"
                except:
                    details["price"] = "Price not available"

                exoffers = driver.find_elements(By.XPATH, "//div[@class='BRgXml']")
                unique_exoffers = [exoffer.text.strip() for exoffer in exoffers]
                details["exchange_offer"] = unique_exoffers if unique_exoffers else "Exchange Offer not available"

                # Click on 'Show more' button to reveal more details if available
                try:
                    show_more_button = driver.find_element(By.XPATH, "//button[@class='_0+FGxP']")
                    show_more_button.click()
                    sleep(2)
                except:
                    pass

                # Get product offers
                offers = driver.find_elements(By.XPATH, "//li[@class='kF1Ml8 col']")
                unique_offers = [offer.text.strip() for offer in offers]
                details["offers"] = unique_offers if unique_offers else "Offers not available"

                # Get product description
                diss = driver.find_elements(By.XPATH, "//li[@class='_7eSDEz']")
                unique_diss = [dis.text.strip() for dis in diss]
                details["description"] = unique_diss if unique_diss else "Description not available"
                
                # Get current date and time
                now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                details["DT"] = now

                # Add product details to dictionary
                products[product_name] = details

                # Incrementing the counter variable
                i+=1
            except Exception as e:
                print(f"Error processing product: {product_url}, Exception: {e}")

    # Write data to CSV file
    with open("unfiltered-data-flipkart.csv", "w", encoding='utf-8', newline="") as csvfile:
        fieldnames = ["Image", "Name", "Price", "Exchange offer", "Offers", "Description", "Date & Time"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for product_name, details in products.items():
            writer.writerow({
                "Image": details["image_url"],
                "Name": details["name"],
                "Price": details["price"],
                "Exchange offer": ", \n".join(details["exchange_offer"]),
                "Offers": ", \n".join(details["offers"]),
                "Description": ", \n".join(details["description"]),
                "Date & Time": details["DT"],
            })

    print("Products saved to productsFK.csv")
    driver.quit()

def scrape_data(websites, phones, max_size):
    # Replace this placeholder with your actual scraping logic
    # It should handle different websites, phone names, and size limits
    print("Started Working")
    #st.write(f"Scraping data from {websites} for phones: {phones[:max_size]} (limited to {max_size} rows)")
    #if websites=="Amazon":
    print("Website",websites)
    print("Phones: ",phones)
    global driver
    driver = webdriver.Chrome()
    # for phone in phones:
    #     print("Started: ",phone)
    #     st.write(f"Scraping data from {websites} for phones: {phones[:max_size]} (limited to {max_size} rows)")
    #     amazon_scraper(phone,max_size)
    #     print("Finished: ",phone)
    for website in websites:
        print(f"Website: {website}")
        for phone in phones:
            print(f"Started: {phone}")
            st.write(f"Scraping data from {website} for phones: {phones[:max_size]} (limited to {max_size} rows)")

            # Perform website-specific scraping logic here (replace with actual implementation)
            if website == "Amazon":
                amazon_scraper(phone, max_size)
            elif website == "Flipkart":
                flipkart_scraper(phone,max_size)
            else:
                # Handle other websites (implementation required)
                st.warning("Scraper not implemented for", website)
                pass

            print(f"Finished: {phone}")

    driver.quit()  # Close WebDriver after scraping is complete

    # Display completion popup with CSV content (assuming successful scraping)
    st.success("Scraping completed!")
    st.write("**Here's a sample of the scraped data:**")
    if "Amazon" in websites:
        filename = 'unfiltered-data-amazon.csv'  # Modify filename as needed
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                # Display a limited number of rows to avoid overwhelming the user interface
                df = pd.read_csv(filename, encoding='utf-8')

                # Limit the number of rows displayed
                limited_df = df.head(max_size)

                # Display the data using st.dataframe for a more interactive table
                st.dataframe(limited_df)
        except FileNotFoundError:
            st.warning("CSV file not found. Scraping might not have been successful.")
    if "Flipkart" in websites:
        filename = 'unfiltered-data-flipkart.csv'  # Modify filename as needed
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                # Display a limited number of rows to avoid overwhelming the user interface
                df = pd.read_csv(filename, encoding='utf-8')

                # Limit the number of rows displayed
                limited_df = df.head(max_size)

                # Display the data using st.dataframe for a more interactive table
                st.dataframe(limited_df)
        except FileNotFoundError:
            st.warning("CSV file not found. Scraping might not have been successful.")        
    # #Insert a completed popup after this
    #Show a sample of the contents in the CSV file
def amazon_scraper(query,max):
    driver.get('https://amazon.in')

    driver.maximize_window()
    input_search = driver.find_element(By.ID, 'twotabsearchtextbox')
    search_button = driver.find_element(By.ID, 'nav-search-submit-button')
    input_search.send_keys(query)
    time.sleep(1)
    search_button.click()

    try:
        brand_refinements = driver.find_element(By.ID, "brandsRefinements")
        brand_list = brand_refinements.find_element(By.CSS_SELECTOR, "ul.a-unordered-list.a-nostyle.a-vertical.a-spacing-medium")
        checkbox_labels = brand_list.find_elements(By.CSS_SELECTOR, "label")
        for label in checkbox_labels:
            checkbox_input = label.find_element(By.CSS_SELECTOR, "input[type='checkbox']")
            if not checkbox_input.is_selected():
                label.click()
    except:
        pass

    product_class = '//div[@data-component-type="s-search-result"]'

    products = []
    page_number = 1
    while True:
        print("Outer loop")
        product_elements = driver.find_elements(By.XPATH, product_class)

        for i in range(0,max):
            product_element = product_elements[i]
            print("Inside Loop")
            try:
                productname = product_element.find_element(By.XPATH, './/span[@class="a-size-medium a-color-base a-text-normal"]').text
                price = product_element.find_element(By.XPATH, './/span[@class="a-price-whole"]').text
            except:
                continue

            try:
                product_link = product_element.find_element(By.XPATH, './/a[@class="a-link-normal s-no-outline"]').get_attribute('href')
                driver.execute_script("window.open('');")
                driver.switch_to.window(driver.window_handles[1])
                driver.get(product_link)
                time.sleep(2)

                offer_details = []
                offer_sections = driver.find_elements(By.CLASS_NAME, 'a-size-base.a-link-emphasis.vsx-offers-count')

                for offer_section in offer_sections:
                    driver.execute_script("arguments[0].click();", offer_section)
                    time.sleep(2)

                    try:
                        side_sheet = driver.find_element(By.ID,'twister-plus-side-sheet-content')
                        main_section = side_sheet.find_element(By.ID,'tp-side-sheet-main-section')
                        offers_list_section = main_section.find_element(By.CLASS_NAME, 'a-section.a-spacing-small.a-spacing-top-small.vsx-offers-desktop-lv__list')
                        offer_items = offers_list_section.find_elements(By.CLASS_NAME, 'a-section.vsx-offers-desktop-lv__item')

                        for offer_item in offer_items:
                            try:
                                offer_text_element = WebDriverWait(offer_item, 10).until(
                                    EC.presence_of_element_located((By.CSS_SELECTOR, "p.a-spacing-mini.a-size-base-plus"))
                                )
                                offer_text = offer_text_element.text
                                offer_details.append(offer_text)
                            except:
                                pass

                        try:
                            view_more_button = side_sheet.find_element(By.CSS_SELECTOR, 'a.a-link-normal.a-spacing-mini')
                            driver.execute_script("arguments[0].click();", view_more_button)
                            time.sleep(2)

                            additional_offers_section = side_sheet.find_element(By.CLASS_NAME, 'a-section.vsx-offers-desktop-lv__list')
                            additional_offer_items = additional_offers_section.find_elements(By.CLASS_NAME, 'a-section.vsx-offers-desktop-lv__item')

                            for offer_item in additional_offer_items:
                                try:
                                    offer_text_element = WebDriverWait(offer_item, 10).until(
                                        EC.presence_of_element_located((By.CSS_SELECTOR, "p.a-spacing-mini.a-size-base-plus"))
                                    )
                                    offer_text = offer_text_element.text
                                    offer_details.append(offer_text)
                                except:
                                    pass
                        except:
                            pass
                    except:
                        pass

                driver.close()
                driver.switch_to.window(driver.window_handles[0])

            except:
                pass

            products.append([productname, price, offer_details])

        print('scraping page', page_number)
        break
        try:
            next_button = driver.find_element(By.CSS_SELECTOR, 'a.s-pagination-item.s-pagination-next.s-pagination-button.s-pagination-separator')
            next_button.click()
            time.sleep(2)
            page_number += 1
        except:
            break

    filename = 'unfiltered-data-amazon.csv'
    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Product Name', 'Price', 'Offers'])
        for product in products:
            writer.writerow(product)

    print(f"Scraped data saved to {filename}")

# Sample phone names (replace with your desired list)
phone_options = [
    "Galaxy S21",
    "Galaxy S21+",
    "Galaxy S21 Ultra",
    "Galaxy Z Fold 3",
    "Galaxy Z Flip 3",
    "Galaxy Note 20",
    "Galaxy Note 20 Ultra",
    "Galaxy Note 10",
    "Galaxy Note 10+",
    "Galaxy Note 10 Lite",
    "Galaxy S20",
    "Galaxy S20+",
    "Galaxy S20 Ultra",
    "Galaxy S20 FE",
    "Galaxy S10",
    "Galaxy S10+",
    "Galaxy S10e",
    "Galaxy S10 Lite",
    "Galaxy A72",
    "Galaxy A52",
    "Galaxy A42",
    "Galaxy A32",
    "Galaxy A22",
    "Galaxy A12",
    "Galaxy A02",
    "Galaxy M62",
    "Galaxy M52",
    "Galaxy M42",
    "Galaxy M32",
    "Galaxy M12",
    "Galaxy M02",
    "Galaxy XCover Pro",
    "Galaxy XCover 5",
    "Galaxy XCover 4s",
    "Galaxy Tab S7",
    "Galaxy Tab S7+",
    "Galaxy Tab S6",
    "Galaxy Tab S6 Lite",
    "Galaxy Tab A7",
    "Galaxy Tab A7 Lite",
    "Galaxy Tab A 10.1",
    "Galaxy Tab A 8.0",
    "Galaxy Tab Active3",
    "Galaxy Watch 4",
    "Galaxy Watch 4 Classic",
    "Galaxy Watch 3",
    "Galaxy Watch Active 2",
    "Galaxy Watch Active",
    "Galaxy Buds Pro",
    "Galaxy Buds Live",
    "Galaxy Buds+",
    "Galaxy Buds",
    "Galaxy Fit 2",
    "Galaxy Fit",
    "Galaxy Fit e",
    "Galaxy Z Fold 2",
    "Galaxy Z Flip",
    "Galaxy Fold",
    "Galaxy Note 9",
    "Galaxy Note 8",
    "Galaxy Note Fan Edition",
    "Galaxy S9",
    "Galaxy S9+",
    "Galaxy S8",
    "Galaxy S8+",
    "Galaxy S7",
    "Galaxy S7 Edge",
    "Galaxy A90 5G",
    "Galaxy A80",
    "Galaxy A70",
    "Galaxy A60",
    "Galaxy A50",
    "Galaxy A40",
    "Galaxy A30",
    "Galaxy A20",
    "Galaxy A10",
    "Galaxy A9",
    "Galaxy A8",
    "Galaxy A7",
    "Galaxy A6",
    "Galaxy A5",
    "Galaxy A3",
    "Galaxy J7",
    "Galaxy J5",
    "Galaxy J3",
    "Galaxy J2",
    "Galaxy J1",
    "Galaxy M10",
    "Galaxy M20",
    "Galaxy M30",
    "Galaxy M40",
    "Galaxy M50",
    "Galaxy M60",
    "Galaxy M70",
    "Galaxy M80",
    "Galaxy M90",
    "Galaxy XCover Pro",
    "Galaxy XCover FieldPro",
    "Galaxy XCover 4",
    "Galaxy XCover 4s",
    "Galaxy Tab S5e",
    "Galaxy Tab S4",
    "Galaxy Tab S3",
    "Galaxy Tab A 8.0 (2019)",
    "Galaxy Tab A 10.1 (2019)",
    "Galaxy Tab A 10.5",
    "Galaxy Tab A 8.0 (2018)",
    "Galaxy Tab A 10.1 (2016)",
    "Galaxy Tab E",
    "Galaxy Tab Active Pro"
]

st.title("Phone Price Scraper")

# Dropdown for website selection
website_options = ["Amazon", "Flipkart"]
selected_website = st.selectbox("Website", website_options)
website_list = [selected_website]

# Multi-select combobox for phone selection
selected_phones = st.multiselect("Phones", phone_options, default=[])

# Input for maximum size
max_size = st.number_input("Maximum Rows to Scrape", min_value=1, max_value=100, value=10)

# Button to trigger scraping
if st.button("Scrape"):
    scrape_data(website_list, selected_phones, max_size)

#st.info("**Note:** This is a placeholder scraping function. Replace it with your implementation.")
