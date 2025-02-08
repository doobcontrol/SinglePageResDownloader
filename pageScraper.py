from http.client import IncompleteRead
import requests

# define Python user-defined exceptions
class WrongUrlException(Exception):
    # _("Raised when the nrl not start with ...")
    pass

class pgScraper:
    """pageScraper class"""

    def __init__(self):
        self.rootDir = ''
        self.illegalChrs = ['#', '%', '&', '{', '}', '\\', '<', '>', '*', '?', \
                       '/', '$', '!', '\'', '"', ':', '@', '+', '`', '|', '=', \
                       'amp;']


    def washPathStr(self, pStr):
        rStr = pStr
        for iChr in self.illegalChrs:
            rStr = rStr.replace(iChr, '')
        return rStr
        
    def downloadOneFile(self, fileUrl, saveFileName):
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

    # for override
    def urlPreHandle(self, pUrl):
        return pUrl

    # for override
    def decodeHtmlContent(self, htmlContent):
        return htmlContent

    # for override
    def getPicList(self, htmlContent):
        return {}

    # for override
    def createSavePath(self, htmlContent):
        return ""
    
    # download method
    def downloadPics(self, pUrl):
        """downloadPics"""
        
        # Making a GET request
        r = requests.get(self.urlPreHandle(pUrl))

        # check status code for response received
        # success code - 200
        if r.status_code == 200:
            htmlContent = self.decodeHtmlContent(r.content)
            picList = self.getPicList(htmlContent)
            savePath = self.createSavePath(htmlContent)
            
            dCount = 0
            for fStr, fileName in picList.items() :
                dSucceed = self.downloadOneFile(fStr, f'{savePath}/{fileName}')
                if dSucceed:
                    print(_('File {fileName} downloaded successfully')\
                          .format(fileName = fileName))
                    dCount += 1
                            
            print(_('{dCount}/{dTotalCount} files downloaded')\
                  .format(dCount = dCount, dTotalCount = len(picList)))
            
        else:
            print(r)
		    
