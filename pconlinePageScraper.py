from pageScraper import pgScraper, WrongUrlException
import os

class pconlinePgScraper(pgScraper):
    """pconlinePgScraper class"""

    # override
    def urlPreHandle(self, inUrl):
        pUrl = inUrl
        if not pUrl.startswith("https://dp.pconline.com.cn/photo/"):
            raise WrongUrlException(_('Url must start with: https://dp.pconline.com.cn/photo/'))
        # check Existence of list_
        if not 'list_' in pUrl:
            pUrl = pUrl[:33] + 'list_' + pUrl[33:]        
        return pUrl

    # override
    def decodeHtmlContent(self, htmlContent):
        return htmlContent.decode('GBK')

    # override
    def getPicList(self, htmlContent):
        picList = {}
        start= 'src="//'
        end = '" onload="bigPicLoaded(this);"'
        fStrA = self.find_allBetween(htmlContent, start, end)
        for fStr in fStrA :
            sStr= "https://" + fStr.replace("_mthumb", "")

            nStrA = fStr.split('/')
            nStr = nStrA[len(nStrA) - 1].replace("_mthumb", "")

            picList[sStr] = nStr
        
        return picList

    # override
    def createSavePath(self, htmlContent):
        # use page title for directory name
        dirMsg = _('directory {pkgDir} created')

        start= '<i id="Jcamerist" class="camerist"><a href="'
        end = '</a>'
        mName = self.find_between(htmlContent, start, end)
        start= '  target="_blank">'
        end = ''
        mName = self.find_between(mName, start, end)        
        mName = self.washPathStr(mName)
        pkgDir = (self.rootDir + mName)
        if not os.path.isdir(pkgDir):
            os.mkdir(pkgDir)
            print(dirMsg.format(pkgDir = pkgDir))


        start= '<meta itemprop="name" content="【'
        end = '】" />'
        pGroupName = self.find_between(htmlContent, start, end)
        pGroupName = self.washPathStr(pGroupName)
        pkgDir = (pkgDir + "/" + pGroupName)
        if not os.path.isdir(pkgDir):
            os.mkdir(pkgDir)
            print(dirMsg.format(pkgDir = pkgDir))
        
        return pkgDir
