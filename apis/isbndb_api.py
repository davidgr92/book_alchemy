import requests

EP_URL = "https://book-cover-api2.p.rapidapi.com/api/public/books/v1/cover/url"
HEADERS = {
    "X-RapidAPI-Key": "66fcd3e4f3msh3df7d95cab486a1p10fa71jsn6033155aa967",
    "X-RapidAPI-Host": "book-cover-api2.p.rapidapi.com"
}
DEFAULT_COVER_PATH = "static/images/empty.jpg"


def get_book_cover_by_isbn(isbn):
    """
    Sends a get request to book-cover api and returns the cover image
    :param isbn: Book isbn value
    :return: Returns image url of the book
    """
    querystring = {"languageCode": "en", "isbn": isbn}
    response = requests.get(EP_URL, headers=HEADERS, params=querystring)
    if response.status_code == 200:
        return response.json()['url']
    else:
        return DEFAULT_COVER_PATH
