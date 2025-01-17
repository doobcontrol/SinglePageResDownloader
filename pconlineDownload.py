import requests
import os
import logging

# define Python user-defined exceptions
class WrongUrlException(Exception):
    "Raised when the nrl not start with https://dp.pconline.com.cn/photo/"
    pass

# download method
def downloadPics(pUrl):
    "downloadPics"
    
    # handle the url
    if not pUrl.startswith("https://dp.pconline.com.cn/photo/"):
        raise WrongUrlException('Url must start with: https://dp.pconline.com.cn/photo/')
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
        Jcamerist=dStr.split('<i id="Jcamerist" class="camerist"><a href="')[1].split('</a>')[0]
        Jcamerist=Jcamerist.split('"  target="_blank">')[1].replace("&nbsp;", "")
        pkgDir = (rootDir + Jcamerist
                  .replace('?', '')
                 .replace('/', '')
                 .replace('*', '')
                 .replace('\\', '')
                 .replace('&amp;x', ''))
        if not os.path.isdir(pkgDir):
            os.mkdir(pkgDir)
            print(f'directory {pkgDir} created')

        pkgDir = (pkgDir + "/" + dStr.split('<meta itemprop="name" content="【')[1].split('】" />')[0].replace("&nbsp;", "")
                 .replace('?', '')
                 .replace('/', '')
                 .replace('*', '')
                 .replace('\\', '')
                 .replace('&amp;', ''))         
        if not os.path.isdir(pkgDir):
            os.mkdir(pkgDir)
            print(f'directory {pkgDir} created')
        
        dCount = 0
        for fStr in fStrA :
            if fStr.endswith("</html>"):
                break;
            
            sStrA = fStr.split('src="//')
            sStr= "https://" + sStrA[len(sStrA) - 1].replace("_mthumb", "")

            nStrA = sStrA[len(sStrA) - 1].split('/')
            nStr = nStrA[len(nStrA) - 1].replace("_mthumb", "")
            
            response = requests.get(sStr)
            
            file_Path = f'{pkgDir}/{nStr}.jpg'
            
            if response.status_code == 200:
                with open(file_Path, 'wb') as file:
                    file.write(response.content)
                    print(f'File {nStr} downloaded successfully')
                    dCount += 1
            else:
                print('Failed to download file')
                        
        print(f'{dCount}/{len(fStrA) - 1} files downloaded')
        
    else:
        print(r)

# Configure the logger
logging.basicConfig(filename='pconlineDownload.log',
                    encoding='utf-8',
                    level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Create a logger object
logger = logging.getLogger(__name__)
logger.info('Start downloading cycle ...')

while True :
    pUrl = input('input url(or q or x to exit): ')
    if pUrl == 'q' or pUrl == 'x':
        break;
    
    try:
        downloadPics(pUrl)
    except WrongUrlException as e:
        print(str(e))
    except Exception as e:
        print(str(e))
        logger.error(str(e))
        
logger.info('The end.\n')
