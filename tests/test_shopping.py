import time
import re
from selenium.webdriver.common.by import By

def test_shopping(driver):
    product = 'samsung galaxy s22'

    # driver = webdriver.Chrome()
    driver.get('https://www.amazon.com/')
    time.sleep(1)

    search_field = driver.find_element(
        By.CSS_SELECTOR, 
        '#twotabsearchtextbox'
    )
    search_field.send_keys(product)

    search_button = driver.find_element(
        By.CSS_SELECTOR, 
        '#nav-search-submit-button'
    )
    search_button.click()

    products = driver.find_elements(
        By.CSS_SELECTOR, 
        'span.rush-component.s-latency-cf-section > '
        'div.s-main-slot.s-result-list.s-search-results.sg-row > div'
    )

    amazon_products = {}
    for element in products:
        try:
            element_name = element.find_element(
                By.CSS_SELECTOR, 
                'span.a-size-medium.a-color-base.a-text-normal'
            )

            if product in element_name.text.lower():
                element_price = element.find_element(
                    By.CSS_SELECTOR, 
                    'span.a-price-whole'
                )
                element_num_comments = element.find_element(
                    By.CSS_SELECTOR,
                    'span.a-size-base.s-underline-text'
                )

                price = re.search(r'[0-9,]+', element_price.text).group()
                price = int(re.sub(',', '', price))
                num_comments = int(
                    re.search(r'[0-9]+', element_num_comments.text).group()
                )

                if not amazon_products.get(num_comments):
                    amazon_products[num_comments] = price
                else:
                    amazon_products[num_comments] = min(
                        amazon_products[num_comments], 
                        price
                    )
        except:
            pass

    print(amazon_products)

    time.sleep(3)


    driver.get('https://www.bestbuy.com/')
    time.sleep(1)

    country_us = driver.find_element(
        By.CSS_SELECTOR, 
        'body > div.page-container > div > div > div > '
        'div:nth-child(1) > div.country-selection > a.us-link'
    )
    country_us.click()
    time.sleep(3)

    search_input = driver.find_element(
        By.CSS_SELECTOR,
        '#gh-search-input'
    )
    search_input.send_keys(product)

    search_button = driver.find_element(
        By.CSS_SELECTOR,
        'button.header-search-button'
    )
    search_button.click()

    products = driver.find_elements(
        By.CSS_SELECTOR,
        'li.sku-item'
    )

    best_buy_products = {}
    for element in products:
        try:
            element_name = element.find_element(
                By.CSS_SELECTOR,
                'h4.sku-title > a'
            )

            is_product = True
            for i in list(product.split(' ')):
                if i not in element_name.text.lower():
                    is_product = False

            if is_product:
                element_price = element.find_element(
                    By.CSS_SELECTOR,
                    'div.priceView-hero-price.priceView-customer-price > span'
                )

                element_num_comments = element.find_element(
                    By.CSS_SELECTOR,
                    'div.c-ratings-reviews.flex.c-ratings-reviews-small.'
                    'align-items-center.gap-50 > span.c-reviews'
                )

                price = re.search(r'[0-9,]+', element_price.text).group()
                price = int(re.sub(',', '', price))
                num_comments = int(
                    re.search(r'[0-9]+', element_num_comments.text).group()
                )
                
                if not best_buy_products.get(num_comments):
                    best_buy_products[num_comments] = price
                else:
                    best_buy_products[num_comments] = min(
                        best_buy_products[num_comments], 
                        price
                    )
        except:
            pass

    print(best_buy_products)

    amazon_price = amazon_products[max(list(amazon_products.keys()))]
    bestbuy_price = best_buy_products[max(list(best_buy_products.keys()))]

    print(amazon_price, bestbuy_price)
    
    assert amazon_price > bestbuy_price
