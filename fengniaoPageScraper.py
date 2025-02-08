from pageScraper import pgScraper, WrongUrlException
import os
import json

class fengniaoPgScraper(pgScraper):
    """fengniaoPgScraper class"""

    # for override
    def urlPreHandle(self, inUrl):
        pUrl = inUrl
        if not pUrl.startswith("https://bbs.fengniao.com/forum/pic/"):
            raise WrongUrlException(_('Url must start with: https://bbs.fengniao.com/forum/pic/'))     
        return pUrl

    # override
    def decodeHtmlContent(self, htmlContent):
        return htmlContent.decode()

    # override
    def getPicList(self, htmlContent):
        start= "eval('('+'"
        end = "'+')');"
        jStr = self.find_between(htmlContent, start, end)   
        json_object = json.loads(jStr)

        picList = {}
        for picDoc in json_object:
            picList[picDoc['downloadPic']] = f'{picDoc['pid']}.jpg'
            
        return picList

    # for override
    def createSavePath(self, htmlContent):
        # use page title for directory name
        dirMsg = _('directory {pkgDir} created')

        start= 'title="" class="name" target="_blank">'
        end = '</a>'
        mName = self.find_between(htmlContent, start, end)   
        mName = self.washPathStr(mName)
        pkgDir = (self.rootDir + mName)
        if not os.path.isdir(pkgDir):
            os.mkdir(pkgDir)
            print(dirMsg.format(pkgDir = pkgDir))
            
        start= "<title>"
        end = "</title>"
        pGroupName = self.find_between(htmlContent, start, end)
        pGroupName = self.washPathStr(pGroupName)
        pkgDir = (pkgDir + "/" + pGroupName)
        if not os.path.isdir(pkgDir):
            os.mkdir(pkgDir)
            print(dirMsg.format(pkgDir = pkgDir))
        
        return pkgDir
