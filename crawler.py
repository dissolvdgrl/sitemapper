import requests


class Crawler:
    def __init__(self, url):
        self.__url = url
        self.__all_urls = [self.__url]
        self.__response_status = 0
        self.__response_text = ""

    def check_connectivity(self):
        response = requests.get(self.__url)
        response.raise_for_status()

        self.__response_status = response.status_code

        if response.status_code == 200:
            self.__response_text = response.text

    def get_response_text(self):
        return self.__response_text

    def get_urls(self):
        current_url = self.__all_urls.pop(0)