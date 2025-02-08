from pageScraper import pgScraper, WrongUrlException
import os

class pconlinePgScraper(pgScraper):
    """pconlinePgScraper class"""

    # for override
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
        fStrA = htmlContent.split('" onload="bigPicLoaded(this);"')
        picList = {}
        for fStr in fStrA :
            if fStr.endswith("</html>"):
                break;
            
            sStrA = fStr.split('src="//')
            sStr= "https://" + sStrA[len(sStrA) - 1].replace("_mthumb", "")

            nStrA = sStrA[len(sStrA) - 1].split('/')
            nStr = nStrA[len(nStrA) - 1].replace("_mthumb", "")

            picList[sStr] = nStr
        
        return picList

    # for override
    def createSavePath(self, htmlContent):
        # use page title for directory name
        dirMsg = _('directory {pkgDir} created')
        illegalChrs = ['#', '%', '&', '{', '}', '\\', '<', '>', '*', '?', \
                       '/', '$', '!', '\'', '"', ':', '@', '+', '`', '|', '=']
        Jcamerist = htmlContent.split('<i id="Jcamerist" class="camerist"><a href="')[1]\
                   .split('</a>')[0]
        Jcamerist = Jcamerist.split('"  target="_blank">')[1].replace("&nbsp;", "")
        for iChr in illegalChrs:
            Jcamerist = Jcamerist.replace(iChr, '')
        pkgDir = (self.rootDir + Jcamerist)
        if not os.path.isdir(pkgDir):
            os.mkdir(pkgDir)
            print(dirMsg.format(pkgDir = pkgDir))

        pGroupName = htmlContent.split('<meta itemprop="name" content="【')[1]\
                     .split('】" />')[0].replace("&nbsp;", "")
        for iChr in illegalChrs:
            pGroupName = pGroupName.replace(iChr, '')
        pkgDir = (pkgDir + "/" + pGroupName)
        if not os.path.isdir(pkgDir):
            os.mkdir(pkgDir)
            print(dirMsg.format(pkgDir = pkgDir))
        
        return pkgDir
