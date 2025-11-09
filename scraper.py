import time
import requests
import schedule
import re
import json
from bs4 import BeautifulSoup

def get_book_data(book_url: str) -> dict:
    """
    Функция, которая возвращает словарь с данными о полученной книге
    Args: book_url (str) путь к странице с книгой
    Returns: Словарь {
        title: Название книги
        price: Стоимость книги
        rating: Рейтинг книги
        count_available: Количество в наличии
        description: Описание
        upc: 
        product_type
        tax
        numbers_of_review
    }    
    """
    # НАЧАЛО ВАШЕГО РЕШЕНИЯ
    res_dict = {}
    response = requests.get(book_url)
    soup = BeautifulSoup(response.text, "html.parser") 
    tag_div = soup.find("div", {"class":"col-sm-6 product_main"})
    reg_price = re.compile(r"\d+(?:\.\d+)?")
    reg_available = re.compile(r"\((\d+).*?\)")
    res_dict["title"] = soup.find("title").get_text().split('|')[0].strip()
    res_dict["price"] = (
        re.findall(reg_price, tag_div
        .find("p", {"class":"price_color"}).text)[0]
        )
    classes = tag_div.find_all("p")
    for next_class in classes:
        if next_class.get("class")[0] == "star-rating":
            res_dict["rating"] =next_class.get("class")[1]
            break    
    instock_availability = (
        tag_div.find("p", {"class":"instock availability"})
        .text.strip()
        )
    res_dict["count_available"] = (
        re.findall(reg_available, instock_availability)[0]
        )
    res_dict["description"] = (
        soup.find("meta", {"name": "description"})
        .get("content").strip()
        )
    tables_rows = (
        soup.find("table", {"class":"table table-striped"})
        .find_all("tr")
        )
    for row in tables_rows:
        if row.find("th").text == "UPC":
            res_dict["upc"] = row.find("td").text
        elif row.find("th").text == "Product Type":
            res_dict["product_type"] = row.find("td").text
        elif row.find("th").text == "Tax":
            res_dict["tax"] = re.findall(reg_price, row.find("td").text)[0] 
        elif row.find("th").text == "Number of reviews":
            res_dict["number_of_reviews"] = row.find("td").text

    return res_dict
    # КОНЕЦ ВАШЕГО РЕШЕНИЯ

book_url = 'http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html'
print(get_book_data(book_url))


def scrape_books(is_save=True):
    """
    Функция для получения данных по всем книгам и записи их 
    в файл artifacts/books_data.txt 
    Args: 
    is_save по-умолчанию True, определяет будет ли записаны данные 
    в файл books_data.txt
    Returns:
    Возвращает список из словарей с данными по каждой книге
    """
    # НАЧАЛО ВАШЕГО РЕШЕНИЯ
    list_book = []
    base_url ="http://books.toscrape.com/catalogue/"
    next_href = "page-1.html"
    response = requests.get(base_url + next_href)
    soup = BeautifulSoup(response.text, "html.parser")
    reg_pages = re.compile(r"of\s(\d+)")
    pager = re.findall(reg_pages, soup.find("li", {"class":"current"}).text)[0] 
    count_page = 1
    while count_page < int(pager):
        all_books_on_page = soup.find("ol", {"class":"row"}).find_all("li")
        for next_book in all_books_on_page:
            book_href = next_book.find("a").get("href")
            data_book = get_book_data(base_url + book_href)
            list_book.append(data_book)
        next_href = (
            soup.find("ul", {"class":"pager"})
            .find("li", {"class":"next"})
            .find("a").get("href")
            )
        response = requests.get(base_url + next_href)
        soup = BeautifulSoup(response.text, "html.parser")
        count_page += 1

    if is_save:
        with open("./artifacts/books_data.txt", "w", encoding="utf-8") as f:
            json.dump(list_book, f, ensure_ascii=False, indent=2)

    return list_book
    # КОНЕЦ ВАШЕГО РЕШЕНИЯ


# res = scrape_books(is_save=True) # Допишите ваши аргументы
# print(type(res), len(res)) # и проверки



if __name__ == "__main__":
    # Запуск скрипта по расписанию на консультации договорились не вставлять
    # schedule.every().day().at("19:35").do(scrape_books)
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1) 
    scrape_books()

    