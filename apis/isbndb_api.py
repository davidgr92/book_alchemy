import requests
from flask import flash

EP_URL = "https://book-cover-api2.p.rapidapi.com/api/public/books/v1/cover/url"
HEADERS = {
    "X-RapidAPI-Key": "66fcd3e4f3msh3df7d95cab486a1p10fa71jsn6033155aa967",
    "X-RapidAPI-Host": "book-cover-api2.p.rapidapi.com"
}
DEFAULT_COVER_PATH = "static/images/empty.jpg"


def get_book_cover_by_isbn(isbn):
    """
    Sends a get request to book-cover api and returns the cover image url
    :param isbn: Book isbn value
    :return: Returns image url of the book
    """
    querystring = {"languageCode": "en", "isbn": isbn}
    try:
        response = requests.get(EP_URL, headers=HEADERS, params=querystring, timeout=15)
        if response.status_code == 200:
            return response.json()['url']
        return DEFAULT_COVER_PATH
    except requests.exceptions.Timeout as timeout:
        flash(f"Timeout while retrieving cover: {timeout}")
        return DEFAULT_COVER_PATH
    except Exception as error:
        flash(f"Error while retrieving cover: {error}")
        return DEFAULT_COVER_PATH
