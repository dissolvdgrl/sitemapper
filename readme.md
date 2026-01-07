# Sitemapper - A basic desktop app to generate XML sitemaps
A simple, easy to use desktop app to generate XML sitemaps for your website.

Please note that this app is still in active development and I'm fixing issues and adding more features.

![Screenshot of a desktop app called Sitemapper running on Ubuntu Linux](https://chilldsgn.com/assets/sitemapper-screenshot.png)

## Installation
You can install this on:
- [Windows 10 & 11](https://sourceforge.net/projects/sitemapper/files/SiteMapper.exe/download)
- [MacOS](https://sourceforge.net/projects/sitemapper/files/SiteMapper.dmg/download)
- [Ubuntu Linux](https://sourceforge.net/projects/sitemapper/files/sitemapper.deb/download)

Download any of the installers above and simply run them. Simple as that.

Please reach out to me if you're having trouble installing this on your system and I'll try to help you.

## Build from source
You'll need PyInstaller to do this. Make sure you install it in this project's virtual environment using ```pip3 install PyInstaller```.

Then you can configure the ```main.spec``` file to suit your needs. 

You can run ```pyinstaller main.spec``` to generate build and dist directories. You'll find an executable for the system you're building on in the dist directory.

## General Notes

This readme will be updated with installation instructions once I've figured it out.

I'm not a Python developer, and this project is for learning purposes. It is also built out of frustration with most sitemap generator tools that have max page limits and make you pay.

Feel free to contact me via my website [https://chilldsgn.com](https://chilldsgn.com) if you have any questions or suggestions.

## Roadmap
1. ~~Add the actual functionality to save the XML output to a user's computer.~~
2. ~~Disable the crawl button when a crawl is in progress.~~
3. ~~Add a timer to remove the status bar messages after some delay.~~
4. ~~Add optional fields to specify lastmod, changefreq.~~
5. Add ability to save sitemaps to edit later when an update is needed. BREAD?
6. Add more stuff to File(New, Open, View All, Exit) menu
7. ~~Add more stuff to Help (About, Report a bug) menu~~
8. ~Add installation instructions for MacOS, Windows, Linux~
9. ~~Include a way to load an XML file saved on disk~~
10. ~~Add warning dialog when closing if the output box contains XML~~
11. Include a shameless plug to descripto.app :P
12. Add auto priority detection based on page depth

FIY I used some LLM generated code, but it was mostly shit, so I fixed what I could and will review at a later stage to fix some residual stupidity.