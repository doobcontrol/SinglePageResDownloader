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
        jStr = htmlContent.split("eval('('+'")[1].split("'+')');")[0]
        json_object = json.loads(jStr)

        picList = {}
        for picDoc in json_object:
            picList[picDoc['downloadPic']] = f'{picDoc['pid']}.jpg'
            
        return picList

    # for override
    def createSavePath(self, htmlContent):
        # use page title for directory name
        dirMsg = _('directory {pkgDir} created')
        illegalChrs = ['#', '%', '&', '{', '}', '\\', '<', '>', '*', '?', \
                       '/', '$', '!', '\'', '"', ':', '@', '+', '`', '|', '=']

        mName = htmlContent.split('title="" class="name" target="_blank">')[1].split('</a>')[0]
        for iChr in illegalChrs:
            mName = mName.replace(iChr, '')
        pkgDir = (self.rootDir + mName)
        if not os.path.isdir(pkgDir):
            os.mkdir(pkgDir)
            print(dirMsg.format(pkgDir = pkgDir))

        pGroupName = htmlContent.split("<title>")[1].split("</title>")[0]

        for iChr in illegalChrs:
            pGroupName = pGroupName.replace(iChr, '')
        pkgDir = (pkgDir + "/" + pGroupName)
        if not os.path.isdir(pkgDir):
            os.mkdir(pkgDir)
            print(dirMsg.format(pkgDir = pkgDir))
        
        return pkgDir
