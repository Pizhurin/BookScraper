BookScraper — это Python-скрипт для автоматического сбора информации о книгах 
с сайта url="http://books.toscrape.com/catalogue/page-{N}.html".  
Он извлекает данные о каждой книге (название, стоимость, рейтинг, количество 
в наличии, описание, универсальный код продукта, тип продукта, налог и количество 
просмотров) и сохраняет результат в JSON-файл.

Описание методов:

get_book_data(book_url: str) -> dict
Извлекает данные о конкретной книге по ссылке на её страницу.  
Возвращает словарь с такими ключами:
  - Название (title)
  - Стоимость (price)
  - Рейтинг (rating)
  - Количество в наличии (count_available)
  - Описание (description)
  - Артикул / UPC (upc)
  - Тип продукта (product_type)
  - Налог (tax)
  - Количество отзывов (number_of_reviews)

scrape_books(is_save=True) -> list[dict]
Обходит все страницы каталога и собирает данные обо всех книгах.  
Если is_save=True, результат сохраняется в artifacts/books_data.txt в формате JSON

Поддерживается запуск скрипта по расписанию в 19:00 (каждый день)

Запуск скрипта:

Для запуска скрипта в bash необходимо выполнить команду python scraper.py

Cтруктура проекта:

books_scraper/
  ├── artifacts/
  │   └── books_data.txt
  ├── notebooks/
  │   └── HW_03_python_ds_2025.ipynb
  ├── scraper.py
  ├── README.md
  ├── tests/
  │   └── test_scraper.py
  ├── .gitignore
  └── requirements.txt
