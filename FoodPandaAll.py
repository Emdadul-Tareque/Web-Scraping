import sys
import requests
import re
import csv
import logging


def get_page_content(url):
    global response
    try:
        response = requests.get(url)
    except requests.exceptions.RequestException as e:
        logging.error(e)

    if response.ok:
        return response.text

    logging.error("Can not get content from URL " + url)
    return ""


def get_restaurant_list(content):
    return res_pat.findall(content)


def get_food_list(content):
    return food_pat.findall(content)


def get_price_list(content):
    return price_pat.findall(content)


def crawl_restaurant(restaurant_url, restaurant_name):
    content = get_page_content(restaurant_url)
    food_result = get_food_list(content)
    price_list = get_price_list(content)

    food_dict = {}

    for item in food_result:
        food_dict["Restaurant name"] = restaurant_name
        food_dict["Food Name"] = item
        print("Scraping: ", item)
    for item in price_list:
        food_dict["Price"] = item

        csv_writer.writerow(food_dict)


def crawl_website():
    url = "https://www.foodpanda.com.bd/city/dhaka"
    host_name = "https://www.foodpanda.com.bd"
    content = get_page_content(url)
    if content == "":
        logging.critical("Got empty content from " + url)
        sys.exit(1)
    restaurant_list = get_restaurant_list(content)

    """category_url, category_name = category_list[0]
    print(category_url)"""

    for category in restaurant_list:
        restaurant_url, restaurant_name = category
        restaurant_url = host_name + restaurant_url
        print("\n")
        print("Restaurant name:", restaurant_name)
        print("URL:", restaurant_url)
        print("\n")

        crawl_restaurant(restaurant_url, restaurant_name)


if __name__ == "__main__":
    host_name1 = "https://www.foodpanda.com.bd"
    res_pat = re.compile(r'<li>\s*<a href="(.*?)".*?<.*?>\s*<.*?=".*?">\s*<.*?>\s*<.*?>(.*?)<', re.S)
    food_pat = re.compile(r'<div class=".*?">\s*<h3 class=".*?">\s*<span>(.*?)</span>')
    price_pat = re.compile(r'<section class="action-bar">.*?<span class="price-discount">(.*?)<', re.S)

    header_fields = ["Restaurant name", "Food Name", "Price"]

    with open("FoodPanda.csv", "w", encoding="UTF-8") as csvf:
        csv_writer = csv.DictWriter(csvf, fieldnames=header_fields)
        csv_writer.writeheader()

        crawl_website()
        print("Crawling Done!")
