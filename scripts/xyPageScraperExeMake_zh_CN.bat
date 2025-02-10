cd ../src/xyPageScraper

pyinstaller -D xyPageScraper.py --add-data ./locales/zh_CN/LC_MESSAGES/xyPageScraper.mo:./locales/zh_CN/LC_MESSAGES

PAUSE