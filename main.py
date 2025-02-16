import sys

from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QToolBar, QWidget, QLineEdit, QFormLayout, QPushButton, QHBoxLayout
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sitemapper")

        # MENU SETUP
        file_action = QAction("New...", self)

        menu = self.menuBar()
        file_menu = menu.addMenu("&File")
        settings_menu = menu.addMenu("&Settings")
        help_menu = menu.addMenu("&Help")

        file_menu.addAction(file_action)

        # SITE CRAWLER
        layout = QHBoxLayout()
        form_container = QWidget()

        self.site_crawler_layout = QFormLayout()
        self.site_url_text = QLineEdit()
        self.crawl_site_button = QPushButton("Crawl site")

        form_container.setLayout(self.site_crawler_layout)

        layout.addWidget(form_container)
        layout.addWidget(self.crawl_site_button)

        self.site_crawler_layout.addRow("Site URL", self.site_url_text)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

app = QApplication(sys.argv)

window = MainWindow()
window.show()
app.exec()



