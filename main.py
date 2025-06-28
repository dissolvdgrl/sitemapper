import os.path
import sys

from PyQt6.QtGui import QAction, QRegularExpressionValidator
from PyQt6.QtCore import QRegularExpression, QStandardPaths, QThread
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
    QStatusBar,
    QFileDialog, QMessageBox
)
from compose.cli.main import filter_services

from CrawlerWorker import CrawlerWorker
from crawler import Crawler


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.thread = None
        self.worker = None
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
        self.status_bar.showMessage("starting crawl, please wait...")
        self.crawl_site_button.setDisabled(True)

        self.thread = QThread()

        crawler = Crawler(self.site_url_text_edit.text())
        self.worker = CrawlerWorker(self.site_url_text_edit.text(), crawler)
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.done.connect(self.hanle_crawl_success)
        self.worker.error.connect(self.hanle_crawl_error)
        self.worker.done.connect(self.thread.quit)
        self.worker.error.connect(self.thread.quit)
        self.worker.done.connect(self.thread.deleteLater)

        self.thread.start()

    def copy_to_clipboard(self):
        xml_plain_text = self.output_box.toPlainText()
        clipboard = QApplication.clipboard()
        clipboard.setText(xml_plain_text)
        self.status_bar.showMessage("Copied to clipboard", 7000)

    def save_xml_file(self):
        caption = "Save sitemap on my device"
        initial_dir = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DocumentsLocation)
        initial_filter = "XML Files (*.xml)"
        filename, selected_filter = QFileDialog.getSaveFileName(
            self,
            caption=caption,
            directory=initial_dir,
            filter=initial_filter,
            initialFilter=initial_filter
        )

        # User cancels, do nothing
        if not filename:
            return

        if os.path.exists(filename):
            confirm = QMessageBox.question(
                self,
                "Warning - You're about to overwrite an existing file",
                f"The file '{filename} already exists. Do you want to overwrite it?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if confirm != QMessageBox.StandardButton.Yes:
                return

        try:
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(self.output_box.toPlainText())
            QMessageBox.information(self, "File saved", f"File saved successfully to:\n{filename}")
        except Exception as exception:
            QMessageBox.critical(self, "Error", f"Failed to save the file:\n{str(exception)}")

        print("Result: ", filename, selected_filter)
        self.status_bar.showMessage("Saved xml file to disk", 7000)

    def hanle_crawl_success(self, xml):
        self.output_box.setPlainText(xml)
        self.save_xml_file_button.setDisabled(False)
        self.copy_output_button.setDisabled(False)
        self.status_bar.showMessage("Site crawled successfully!", 7000)
        self.crawl_site_button.setDisabled(False)

    def hanle_crawl_error(self, message):
        self.status_bar.showMessage(message, 700)
        self.crawl_site_button.setDisabled(False)

app = QApplication(sys.argv)

window = MainWindow()
window.show()
app.exec()



