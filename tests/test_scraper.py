from scraper import get_book_data, scrape_books

def test_type_get_book_data():
    url = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
    dict_data = get_book_data(url)    
    assert isinstance(dict_data, dict), "Тип не словарь"
    

def test_count_key_get_book_data():
    url = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
    dict_data = get_book_data(url)  
    assert len(dict_data.keys()) == 9, "Не совпадает количество ключей в словаре" 
        

def test_key_names_book_data():
    url = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
    dict_data = get_book_data(url)   
    assert dict_data["title"] == "A Light in the Attic", "Неверно title"
    assert dict_data["price"] == "51.77", "Неверно price"
    assert dict_data["rating"] == "Three", "Неверно rating"
    assert dict_data["count_available"] == "22", "Неверно count_available"
    assert (
        dict_data["description"].startswith("It's hard to imagine")
        ), "Неверно description"
    assert dict_data["upc"] == "a897fe39b1053632", "Неверно upc"
    assert dict_data["product_type"] == "Books", "Неверно product_type"
    assert dict_data["tax"] == "0.00", "Неверно tax"
    assert dict_data["number_of_reviews"] == "0", "Неверно number_of_reviews"


# Не разбил на несколько тестов, для экономии времени на проверку тестов
def test_scrape_books():
    list_data = scrape_books(False)
    assert isinstance(list_data, list), "Тип не список"
    assert len(list_data) == 980, "Не все книги найдены"
    assert isinstance(list_data[0], dict), "Элементы списка не словари"
    assert len(list_data[0].keys()) == 9, "Не совпадает количество ключей" 
    expected_keys = {
        "title", 
        "price", 
        "rating", 
        "count_available", 
        "description", 
        "upc", 
        "product_type", 
        "tax", 
        "number_of_reviews"
        }
    real_keys = set(list_data[0].keys())
    assert (
        expected_keys.intersection(real_keys) == expected_keys
        ), "Ключи в словарях не соответствуют ожидаемым"
    