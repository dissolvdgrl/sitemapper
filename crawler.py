import requests
from bs4 import BeautifulSoup


class Crawler:
    def __init__(self, url):
        self.__url = url
        self.__all_urls = [self.__url]
        self.__response_text = ""

    def check_connectivity(self):
        response = requests.get(self.__url)
        response.raise_for_status()

        self.__response_text = response.text

        return response.status_code

    def get_response_text(self):
        return self.__response_text

    def init_soup(self, response_text):
        return BeautifulSoup(response_text, "html.parser")

    def get_urls(self):
        current_url = self.__all_urls.pop(0)
        soup = self.init_soup(self.__response_text)
        link_elements = soup.select("a[href]")
        print(link_elements)
