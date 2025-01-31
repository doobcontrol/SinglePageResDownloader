from http.client import IncompleteRead
import requests
import sys
import os
import logging
import gettext

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
appname = 'pconlineDownload'
# Set up Gettext
en_i18n = gettext.translation(appname, locale_dir, fallback=True)
# Create the "magic" function
en_i18n.install()

# define Python user-defined exceptions
class WrongUrlException(Exception):
    _("Raised when the nrl not start with https://dp.pconline.com.cn/photo/")
    pass

def downloadOneFile(fileUrl, saveFileName):
    tryTimes = 0
    while True:
        try: 
            r = requests.get(fileUrl) 
            r.raise_for_status() 
            with open(saveFileName, 'wb') as file:
                file.write(r.content)
                
            return True
        except IncompleteRead as e: 
            if tryTimes < 9:
                tryTimes += 1
                print(_("network interruption, retry"))
            else:
                print(_("network interruption 10 times, I'm give up"))
                return False
        except requests.HTTPError as e:
            if r.status_code == 424:
                print(_('Failed to download file'))
            else:
                print(str(e))
                print(r)
            return False
        except Exception as e:
            print(str(e))
            return False

# download method
def downloadPics(pUrl):
    "downloadPics"
    
    # handle the url
    if not pUrl.startswith("https://dp.pconline.com.cn/photo/"):
        raise WrongUrlException(_('Url must start with: https://dp.pconline.com.cn/photo/'))
    # check Existence of
    if not 'list_' in pUrl:
        pUrl = pUrl[:33] + 'list_' + pUrl[33:]
    
    # Making a GET request
    r = requests.get(pUrl)

    rootDir = '' # 'Z:/Windows11x64TempForDbCrack/temp/'

    # check status code for response received
    # success code - 200
    if r.status_code == 200:
        # print content of request
        dStr = r.content.decode('GBK')
        fStrA = dStr.split('" onload="bigPicLoaded(this);"')

        
        # use page title for directory name
        dirMsg = _('directory {pkgDir} created')
        illegalChrs = ['#', '%', '&', '{', '}', '\\', '<', '>', '*', '?', \
                       '/', '$', '!', '\'', '"', ':', '@', '+', '`', '|', '=']
        Jcamerist=dStr.split('<i id="Jcamerist" class="camerist"><a href="')[1]\
                   .split('</a>')[0]
        Jcamerist=Jcamerist.split('"  target="_blank">')[1].replace("&nbsp;", "")
        for iChr in illegalChrs:
            Jcamerist = Jcamerist.replace(iChr, '')
        pkgDir = (rootDir + Jcamerist)
        if not os.path.isdir(pkgDir):
            os.mkdir(pkgDir)
            print(dirMsg.format(pkgDir = pkgDir))

        pGroupName = dStr.split('<meta itemprop="name" content="【')[1]\
                     .split('】" />')[0].replace("&nbsp;", "")
        for iChr in illegalChrs:
            pGroupName = pGroupName.replace(iChr, '')
        pkgDir = (pkgDir + "/" + pGroupName)
        if not os.path.isdir(pkgDir):
            os.mkdir(pkgDir)
            print(dirMsg.format(pkgDir = pkgDir))
        
        dCount = 0
        for fStr in fStrA :
            if fStr.endswith("</html>"):
                break;
            
            sStrA = fStr.split('src="//')
            sStr= "https://" + sStrA[len(sStrA) - 1].replace("_mthumb", "")

            nStrA = sStrA[len(sStrA) - 1].split('/')
            nStr = nStrA[len(nStrA) - 1].replace("_mthumb", "")
            
            dSucceed = downloadOneFile(sStr, f'{pkgDir}/{nStr}.jpg')
            if dSucceed:
                print(_('File {nStr} downloaded successfully').format(nStr = nStr))
                dCount += 1
                        
        print(_('{dCount}/{dTotalCount} files downloaded')\
              .format(dCount = dCount, dTotalCount = len(fStrA) - 1))
        
    else:
        print(r)
		    
# Configure the logger
logging.basicConfig(filename='pconlineDownload.log',
                    encoding='utf-8',
                    level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Create a logger object
logger = logging.getLogger(__name__)
logger.info(_('Start downloading cycle ...'))

while True :
    pUrl = input(_('input url(or q or x to exit): '))
    if pUrl == 'q' or pUrl == 'x':
        break;
    
    try:
        downloadPics(pUrl)
    except WrongUrlException as e:
        print(str(e))
    except Exception as e:
        print(str(e))
        logger.error(
            str(e),
            exc_info=True
        )
        
logger.info(_('The end.\n'))
