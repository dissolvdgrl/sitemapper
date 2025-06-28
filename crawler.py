import time
from typing import Set, List
from urllib.parse import urlparse, urljoin

import requests
from PyQt6.QtCore import pyqtSignal
from bs4 import BeautifulSoup


class Crawler:
    def __init__(self, url):
        self.__soup = None
        self.__root_url = url.rstrip('/')
        self.__domain = urlparse(self.__root_url).netloc # internal urls only
        self.__all_urls: Set[str] = {self.__root_url}
        self.__crawled_urls: Set[str] = set()
        self.__failed_urls: Set[str] = set()
        self.__response_text = ""
        self.__delay: float = 1.0
        self.__session = requests.Session()
        self.__session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        done = pyqtSignal(str)
        error = pyqtSignal(str)

    def check_connectivity(self) -> int:
        try:
            response = self.__session.get(self.__root_url, timeout=10)
            response.raise_for_status()

            self.__response_text = response.text
            self.__soup = BeautifulSoup(self.__response_text, "html.parser")
            return response.status_code

        except requests.RequestException as exception:
            print(f"Error connecting to {self.__root_url}: {exception}")
            raise

    def get_response_text(self) -> str:
        return self.__response_text

    def visit_page(self, url: str) -> bool:
        try:
            time.sleep(self.__delay)
            response = self.__session.get(url, timeout=10)

            if response.status_code == 200:
                self.__response_text = response.text
                self.__soup = BeautifulSoup(self.__response_text, "html.parser")
                self.__crawled_urls.add(url)
                return True
            else:
                print(f"Failed to crawl {url}: Status {response.status_code}")
                self.__failed_urls.add(url)
                return False
        except requests.RequestException as exception:
            print(f"Error crawling {url}: {exception}")
            self.__failed_urls.add(url)
            return False

    def get_page_urls(self) -> List[str]:

        if not self.__soup:
            return []

        found_urls = []
        link_elements = self.__soup.find_all("a", href=True)

        for link in link_elements:
            href = link["href"].strip()

            if not href or href.startswith('#') or href.startswith('javascript:') or href.startswith('mailto:') or href == '/':
                continue

            absolute_url = urljoin(self.__root_url, href)

            if self._is_internal_url(absolute_url):
                clean_url = absolute_url.split('#')[0].split('?')[0]

                # Normalise the URL
                parsed = urlparse(clean_url)
                if parsed.path == '' or parsed.path == '/':
                    clean_url = f"{parsed.scheme}://{parsed.netloc}/"
                else:
                    clean_url = clean_url.rstrip('/')

                if clean_url not in self.__all_urls and clean_url not in self.__crawled_urls:
                    found_urls.append(clean_url)
                    self.__all_urls.add(clean_url)

        return found_urls

    def crawl_all(self) -> bool:
        print(f"Starting crawl of {self.__root_url}")

        try:
            self.check_connectivity()
        except requests.RequestException:
            print(f"Couldn't connect to root URL, crawling aborted")
            return False

        urls_to_process = list(self.__all_urls - self.__crawled_urls)

        while urls_to_process:
            current_url = urls_to_process.pop(0)

            if current_url not in self.__crawled_urls or current_url not in self.__all_urls:
                if self.visit_page(current_url):
                    new_urls = self.get_page_urls()

                    for new_url in new_urls:
                        if new_url not in self.__crawled_urls and new_url not in urls_to_process:
                            urls_to_process.append(new_url)

        print(f"Crawl completed. Found {len(self.__all_urls)} total URLs, crawled {len(self.__crawled_urls)} pages")
        return True

    def get_all_urls(self) -> List[str]:
        return sorted(list(self.__all_urls))

    def get_crawled_urls(self) -> List[str]:
        return sorted(list(self.__crawled_urls))

    def get_failed_urls(self) -> List[str]:
        return sorted(list(self.__failed_urls))

    def get_uncrawled_urls(self) -> list[str]:
        return sorted(list(self.__all_urls - self.__crawled_urls - self.__failed_urls))

    def _is_internal_url(self, url: str) -> bool:
        try:
            parsed_url = urlparse(url)
            return parsed_url.netloc == self.__domain or parsed_url.netloc == ""
        except Exception as exception:
            print(f"Not an internal URL: {exception}")
            return False

    def generate_sitemap_xml(self, include_metadata: bool = True) -> str:
        xml_lines = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            '<!-- Sitemap generated by SiteMapper v1.0 (https://github.com/dissolvdgrl/sitemapper) -->',
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        ]

        for url in self.get_crawled_urls():
            xml_lines.append('   <url>')
            xml_lines.append(f'      <loc>{url}</loc>')

            if include_metadata:
                # You can customize these values based on your needs
                xml_lines.append('      <lastmod>2024-01-01</lastmod>')
                xml_lines.append('      <changefreq>monthly</changefreq>')
                xml_lines.append('      <priority>0.8</priority>')

            xml_lines.append('   </url>')

        xml_lines.append('</urlset>')
        return '\n'.join(xml_lines)