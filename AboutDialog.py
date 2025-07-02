from PyQt6.QtWidgets import \
    QDialog, QVBoxLayout, \
    QLabel


class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__()

        self.resize(450, 275)
        self.setWindowTitle("About Sitemapper")

        heading = QLabel("<span style='font:bold;font-size:20px;'>About Sitemapper</span>")
        version = QLabel("v1.0")
        developed_by = QLabel("Developed by Christie Hill")
        blurb1 = QLabel("Sitemapper is a small desktop application that generates XML sitemaps for your websites.")
        blurb2 = QLabel("I built it to be easy to use and can run on multiple operating systems. ")
        found_bug = QLabel("<span style='font:bold;font-size:16px;'>Found a bug?</span>")
        contact_me = QLabel("Contact me by visiting my website: <a href='https://chilldsgn.com'>chilldsgn.com</a>")
        contact_me.setOpenExternalLinks(True)
        github = QLabel("Source code: <a href='https://github.com/dissolvdgrl/sitemapper'>https://github.com/dissolvdgrl/sitemapper</a>")
        github.setOpenExternalLinks(True)

        layout_vertical = QVBoxLayout()

        layout_vertical.addWidget(heading)
        layout_vertical.addWidget(version)
        layout_vertical.addWidget(blurb1)
        layout_vertical.addWidget(blurb2)
        layout_vertical.addStretch(1)
        layout_vertical.addWidget(developed_by)
        layout_vertical.addWidget(github)
        layout_vertical.addStretch(1)
        layout_vertical.addWidget(found_bug)
        layout_vertical.addWidget(contact_me)
        layout_vertical.addStretch(1)

        self.setLayout(layout_vertical)