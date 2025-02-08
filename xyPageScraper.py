import sys
import os
import logging
import gettext
from pageScraper import WrongUrlException

if sys.platform.startswith('win'):
    if os.getenv('LANG') is None:
        import ctypes
        import locale
        windll = ctypes.windll.kernel32
        os.environ['LANG'] = locale.windows_locale[windll.GetUserDefaultUILanguage()]

# check if is running in a PyInstaller bundle
locale_dir = './locales'
if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    locale_dir = './_internal/locales'
    
# Set up translation
appname = 'xyPageScraper'
# Set up Gettext
en_i18n = gettext.translation(appname, locale_dir, fallback=True)
# Create the "magic" function
en_i18n.install()
		    
# Configure the logger
logging.basicConfig(filename='xyPageScraper.log',
                    encoding='utf-8',
                    level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Create a logger object
logger = logging.getLogger(__name__)
logger.info(_('Start downloading cycle ...'))


while True :
    print(_("[0] pconline"))
    print(_("[1] fengniao"))
    pUrl = input(_('select resource site(or q or x to exit): '))
    if pUrl == 'q' or pUrl == 'x':
        break
    elif pUrl == '0' or pUrl == '1':
        scraper = None
        if pUrl == '0':
            from pconlinePageScraper import pconlinePgScraper
            scraper = pconlinePgScraper()
        elif pUrl == '1':
            pass
        
        while True :
            pUrl = input(_('input url(or q or x to exit): '))
            if pUrl == 'q' or pUrl == 'x':
                break;
            
            try:
                scraper.downloadPics(pUrl)
            except WrongUrlException as e:
                print(str(e))
            except Exception as e:
                print(str(e))
                logger.error(
                    str(e),
                    exc_info=True
                )
                
    else:
        print(_("error input. Please retry"))
        
logger.info(_('The end.\n'))
