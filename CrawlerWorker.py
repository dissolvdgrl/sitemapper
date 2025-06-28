from PyQt6.QtCore import QThread, pyqtSignal, QObject

class CrawlerWorker(QObject):
    done = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, url, crawler):
        super().__init__()
        self.url = url
        self.crawler = crawler

    def run(self):
        if self.crawler.check_connectivity() == 200:
            crawled = self.crawler.crawl_all()

            if (crawled):
                xml = self.crawler.generate_sitemap_xml(True)
                self.done.emit(xml)
            else:
                self.error.emit("The website you provided couldn't be crawled.")
        else:
            self.error.emit("The website you provided couldn't be reached.")