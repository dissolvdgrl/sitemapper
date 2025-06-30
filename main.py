import os.path
import sys

from PyQt6.QtGui import QAction, QRegularExpressionValidator, QCloseEvent
from PyQt6.QtCore import QRegularExpression, QStandardPaths, QThread
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QLineEdit,
    QFormLayout,
    QPushButton,
    QHBoxLayout,
    QPlainTextEdit,
    QVBoxLayout,
    QStatusBar,
    QFileDialog,
    QMessageBox,
    QDateEdit,
    QComboBox, QDialog
)
from compose.cli.main import filter_services

from AboutDialog import \
    AboutDialog
from CrawlerWorker import CrawlerWorker
from crawler import Crawler


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.thread = None
        self.worker = None
        self.setWindowTitle("Sitemapper")
        self.resize(1024, 400)
        self.selected_change_freq = ""

        # URL Pattern Regex
        self.url_regex = QRegularExpression(r'^https:\/\/(www\.)?[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\/?$')
        url_regex_validator = QRegularExpressionValidator(self.url_regex)

        # MENU SETUP
        file_action_new = QAction("New...", self)
        file_action_open = QAction("Open...", self)
        file_action_open.triggered.connect(self.open_xml_sitemap)
        file_action_help_about = QAction("About Sitemapper", self)
        file_action_help_about.triggered.connect(self.show_about)
        file_action_help_report_bug = QAction("Report a bug", self)

        menu = self.menuBar()
        file_menu = menu.addMenu("&File")
        help_menu = menu.addMenu("&Help")

        file_menu.addAction(file_action_new)
        file_menu.addSeparator()
        file_menu.addAction(file_action_open)
        help_menu.addAction(file_action_help_about)
        help_menu.addAction(file_action_help_report_bug)

        # LAYOUTS
        layout = QHBoxLayout()
        output_container = QVBoxLayout()
        form_container = QWidget()

        # FORMS
        self.main_layout = QFormLayout()
        self.site_url_text_edit = QLineEdit()
        self.site_url_text_edit.setPlaceholderText("https://mysite.com")
        self.site_url_text_edit.setValidator(url_regex_validator)
        self.last_mod_text_edit = QDateEdit()
        self.change_freq_edit = QComboBox()
        self.change_freq_edit.setToolTip("Change frequency tells search engines how often a page’s content updates.")
        self.change_freq_edit.addItems(["Always", "Hourly", "Daily", "Weekly", "Monthly", "Yearly", "never"])
        self.change_freq_edit.setCurrentIndex(3) # Set the default to Weekly

        self.change_freq_edit.currentIndexChanged.connect(self.set_change_freq)

        # BUTTONS
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

        self.main_layout.addRow("Site URL*", self.site_url_text_edit)
        self.main_layout.addRow("Last modified", self.last_mod_text_edit)
        self.main_layout.addRow("Change frequency", self.change_freq_edit)
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

    def set_change_freq(self):
        self.selected_change_freq = self.change_freq_edit.currentText()

    def start_crawl(self):
        self.status_bar.showMessage("starting crawl, please wait...")
        self.crawl_site_button.setDisabled(True)

        self.thread = QThread()

        crawler = Crawler(self.site_url_text_edit.text(), self.last_mod_text_edit.text(), self.selected_change_freq)
        self.worker = CrawlerWorker(self.site_url_text_edit.text(), crawler)
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.done.connect(self.handle_crawl_success)
        self.worker.error.connect(self.handle_crawl_error)
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
            directory=f"{initial_dir}/untitled.xml",
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

    def handle_crawl_success(self, xml):
        self.output_box.setPlainText(xml)
        self.save_xml_file_button.setDisabled(False)
        self.copy_output_button.setDisabled(False)
        self.status_bar.showMessage("Site crawled successfully!", 7000)
        self.crawl_site_button.setDisabled(False)

    def handle_crawl_error(self, message):
        self.status_bar.showMessage(message, 700)
        self.crawl_site_button.setDisabled(False)

    def closeEvent(self, event: QCloseEvent):
        if self.output_box.toPlainText() != "":
            response = QMessageBox.question(
                self,
                "Confirm Quit", "Are you sure you want to quit? Any unsaved progress will be lost.",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )

            if response == QMessageBox.StandardButton.Yes:
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()

    def open_xml_sitemap(self):
        caption = "Open a sitemap on your device"
        initial_dir = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DocumentsLocation)
        initial_filter = "XML Files (*.xml)"
        filename, selected_filter = QFileDialog.getOpenFileName(
            self,
            caption=caption,
            directory=initial_dir,
            filter=initial_filter,
            initialFilter=initial_filter
        )

        # User cancels, do nothing
        if not filename:
            return

        if filename:
            with open(filename, "r") as file:
                file_contents = file.read()
            self.output_box.setPlainText(file_contents)

    def show_about(self):
        dialog = AboutDialog(self)
        dialog.exec()

app = QApplication(sys.argv)

window = MainWindow()
window.show()
sys.exit(app.exec())



