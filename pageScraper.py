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
                       'amp;', '&nbsp;']

    # Modify based on the code generated by Gemini
    def findIndex_between(self, text, start, end, startSearch = 0):
        try:
            start_index = startSearch
            end_index = len(text)

            if len(start) != 0 :
                start_index = text.index(start, start_index) + len(start)
            if len(end) != 0 :
                end_index = text.index(end, start_index)

            # check if substring between start_index and end_index contains start
            if len(start) != 0 :
                start_indexIn = text.rfind(start, start_index, end_index)
                if start_indexIn != -1:
                    start_index = start_indexIn + len(start)
                    
            return (start_index, end_index)
        except ValueError:
            return None

    def find_between(self, text, start, end, startSearch = 0):
        retIndex = self.findIndex_between(text, start, end, startSearch)
        if retIndex is None:
            return None
        else:
            return text[retIndex[0]:retIndex[1]]
     
    def find_allBetween(self, text, start, end, startSearch = 0):
        findList = []
        beginIndex = startSearch
        endLen = len(end)
        while True: 
            retIndex = self.findIndex_between(text, start, end, beginIndex)
            if retIndex is None:
                break;
            else:
                findList.append(text[retIndex[0]:retIndex[1]])
            beginIndex = retIndex[1] + endLen

        return findList
            
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
		    
