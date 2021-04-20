# #!/usr/bin/env python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
import logging
import time

# Start the browser and login with standard_user
def login (user, password):

    logging.basicConfig(filename='test.log', level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

    logging.info('Starting the Chrome browser')
    options = ChromeOptions()
    options.add_argument("--headless") 

    driver = webdriver.Chrome(options=options)
    # Test login
    logging.info('Chrome started successfully. Navigating to the Saucedemo page')
    driver.get('https://www.saucedemo.com/')
    logging.info('Login in with username:' + user + " and password: "+password )
    driver.find_element_by_css_selector("input[id='user-name']").send_keys(user)
    driver.find_element_by_css_selector("input[id='password']").send_keys(password)
    driver.find_element_by_css_selector("input[id='login-button']").click()
    time.sleep(2)
    results = driver.find_element_by_css_selector("div[class='header_secondary_container'] > span[class='title']").text
    assert "PRODUCTS" in results, "Expected Products but was " + results
    logging.info("Successfully logged in as " + user)

    # Test adding items to cart
    logging.info("Starting selecting products.")
    product_items = driver.find_elements_by_css_selector("div[class='inventory_list'] > div[class='inventory_item']")
    assert len(product_items) == 6
    logging.info("Found 6 product items.")    
    add_item_buttons = driver.find_elements_by_css_selector("div[class='pricebar'] > button.btn_primary.btn_inventory")
    for i in range(6):
        product_item_name = driver.find_element_by_css_selector("a[id='item_" + str(i) + "_title_link'] > div[class='inventory_item_name']")
        add_item_buttons[i].click()
        logging.info("Added to shopping cart: " + product_item_name.text)

    path_shopping_cart_link = "div[id='shopping_cart_container'] > a[class='shopping_cart_link']"
    path_shopping_cart_badge = path_shopping_cart_link + " > span[class='shopping_cart_badge'"
    total_items_added = driver.find_element_by_css_selector(path_shopping_cart_badge).text
    assert '6' == total_items_added
    logging.info("Succesfully added to shopping cart: 6 items in total")

    # Test Removiving items from the cart
    logging.info("Going to the cart")
    driver.find_element_by_css_selector(path_shopping_cart_link).click()
    time.sleep(2)
    cart_title_element = "div[id='header_container'] > div[class='header_secondary_container'] > span[class='title']"
    title = driver.find_element_by_css_selector(cart_title_element).text
    assert 'YOUR CART' in title, "Expected YOUR CART but was " + title
    logging.info("Successfully entered the shopping cart page.")

    remove_item_buttons = driver.find_elements_by_css_selector("div[class='item_pricebar'] > button.btn.cart_button")
    items_names = []
    for i in range(6):
        shopping_cart_item_name = driver.find_element_by_css_selector("a[id='item_" + str(i) + "_title_link'] > div[class='inventory_item_name']").text
        items_names.append(shopping_cart_item_name)
    i = 0
    for remove_button in remove_item_buttons:
        remove_button.click()
        logging.info("Removed an item from shopping cart: " + items_names[i])
        i+=1
    shopping_cart_total_items = driver.find_elements_by_css_selector(path_shopping_cart_badge)
    assert 0 == len(shopping_cart_total_items)
    logging.info("Succesfully removed all items from shopping cart.")

login('standard_user', 'secret_sauce')

