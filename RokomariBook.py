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


def get_category_list(content):
    return cate_pat.findall(content)


def get_book_list(content):
    return book_pat.findall(content)


def crawl_category(category_url, category_name):
    content = get_page_content(category_url)
    book_result = get_book_list(content)

    book_dict = {}

    for item in book_result:
        book_dict["Category"] = category_name
        book_dict["Name"] = item[1]
        book_dict["Author"] = item[2]
        book_dict["Price"] = item[3]
        book_dict["URL"] = host_name1 + item[0]
        print("Scraping: ", item[1])

        csv_writer.writerow(book_dict)


def crawl_website():
    url = "https://www.rokomari.com/book"
    host_name = "https://www.rokomari.com"
    content = get_page_content(url)
    if content == "":
        logging.critical("Got empty content from " + url)
        sys.exit(1)
    category_list = get_category_list(content)

    """category_url, category_name = category_list[0]
    print(category_url)"""

    for category in category_list:
        category_url, category_name = category
        category_url = host_name + category_url
        print("\n")
        print("Category Name:", category_name)
        print("URL:", category_url)
        print("\n")

        crawl_category(category_url, category_name)


if __name__ == "__main__":
    host_name1 = "https://www.rokomari.com"
    cate_pat = re.compile(r'<li><a href="(.*?)>(.*?)</a></li>')
    book_pat = re.compile(r'<a href="(.*?)"\s*.*?<div class="book-text-area">\s*<p class="book-title">(.*?)</p>\s*<p '
                          r'class="book-author">(.*?)</p>\s*.*?<p '
                          r'class="book-price">(.*?)\s*<', re.S)

    header_fields = ["Category", "Name", "Author", "Price", "URL"]

    with open("Rokomari_booklist0411.csv", "w", encoding="UTF-8") as csvf:
        csv_writer = csv.DictWriter(csvf, fieldnames=header_fields)
        csv_writer.writeheader()

        crawl_website()
        print("Crawling Done!")
