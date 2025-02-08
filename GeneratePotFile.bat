dir .\*.py /L /B /S > list
xgettext --files-from=list -d xyPageScraper -s -o xyPageScraper.pot
del list

PAUSE