import sys

from PyQt6.QtGui import QAction, QRegularExpressionValidator
from PyQt6.QtCore import QRegularExpression
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QToolBar,
    QWidget,
    QLineEdit,
    QFormLayout,
    QPushButton,
    QHBoxLayout,
    QPlainTextEdit,
    QVBoxLayout,
    QStatusBar
)

from crawler import Crawler


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sitemapper")
        self.resize(1024, 400)

        # URL Pattern Regex
        self.url_regex = QRegularExpression(r'^https:\/\/(www\.)?[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\/?$')
        url_regex_validator = QRegularExpressionValidator(self.url_regex)

        # MENU SETUP
        file_action = QAction("New...", self)

        menu = self.menuBar()
        file_menu = menu.addMenu("&File")
        settings_menu = menu.addMenu("&Settings")
        help_menu = menu.addMenu("&Help")

        file_menu.addAction(file_action)

        # LAYOUTS
        layout = QHBoxLayout()
        output_container = QVBoxLayout()
        form_container = QWidget()

        # BUTTONS & FORMS
        self.main_layout = QFormLayout()
        self.site_url_text_edit = QLineEdit()
        self.site_url_text_edit.setPlaceholderText("https://mysite.com")
        self.site_url_text_edit.setValidator(url_regex_validator)

        self.crawl_site_button = QPushButton("Crawl site")
        self.copy_output_button = QPushButton("Copy to clipboard")
        self.save_xml_file_button = QPushButton("Save XML file")

        self.crawl_site_button.setDisabled(True)
        self.copy_output_button.setDisabled(True)
        self.save_xml_file_button.setDisabled(True)

        # CONNECT BUTTON & LINE EDIT SIGNALS
        self.site_url_text_edit.textEdited.connect(self.url_added)
        self.crawl_site_button.clicked.connect(self.start_crawl)
        self.copy_output_button.clicked.connect(self.copy_to_clipboard)
        self.save_xml_file_button.clicked.connect(self.save_xml_file)

        # OUTPUT BOX
        self.output_box = QPlainTextEdit()
        self.output_box.setReadOnly(True)
        self.output_box.setPlaceholderText("Your XML sitemap will be created here")

        # STATUS BAR
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        form_container.setLayout(self.main_layout)
        layout.addWidget(form_container)

        self.main_layout.addRow("Site URL", self.site_url_text_edit)
        self.main_layout.addRow(self.crawl_site_button)

        output_container.addWidget(self.output_box)
        output_container.addWidget(self.copy_output_button)
        output_container.addWidget(self.save_xml_file_button)
        layout.addLayout(output_container)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def url_added(self):
        url = self.site_url_text_edit.text()
        match = self.url_regex.match(url)

        if match.hasMatch():
            self.crawl_site_button.setDisabled(False)
        else:
            self.crawl_site_button.setDisabled(True)

    def start_crawl(self):
        self.crawl_site_button.setDisabled(True)
        self.status_bar.showMessage("starting crawl, please wait...")

        crawler = Crawler(self.site_url_text_edit.text())

        if crawler.check_connectivity() == 200:
            self.status_bar.showMessage("we've got green")
            crawled = crawler.crawl_all()

            if crawled:
                xml = crawler.generate_sitemap_xml(True)
                if xml:
                    self.save_xml_file_button.setDisabled(False)
                    self.copy_output_button.setDisabled(False)
                self.output_box.setPlainText(xml)
            else:
                self.status_bar.showMessage("we couldn't crawl the website you provided")


            self.crawl_site_button.setDisabled(False)

    def copy_to_clipboard(self):
        xml_plain_text = self.output_box.toPlainText()
        clipboard = QApplication.clipboard()
        clipboard.setText(xml_plain_text)
        self.status_bar.showMessage("Copied to clipboard")

    def save_xml_file(self):
        self.status_bar.showMessage("Saved xml file to disk")

app = QApplication(sys.argv)

window = MainWindow()
window.show()
app.exec()



