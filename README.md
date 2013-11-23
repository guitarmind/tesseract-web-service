tesseract-web-service
=====================

An implementation of RESTful web service for tesseract-OCR, based on http://wolfpaulus.com/jounal/android-journal/android-and-ocr/

The HTTP server is implemented using tornado.
Currently only accept uploading files or image url with .png extension.
You can modify ***tesseractserver.py*** and ***tesseractapi.py*** to support more formats.




####tsseract Installation on Ubuntu 12.04 LTS

    sudo apt-get install python-tornado
    sudo apt-get install python-imaging
    sudo apt-get install tesseract-ocr


####How to start tesseract-web-service
Create two folders to keep temp files

    mkdir /tmp/ocr
    mkdir /tmp/ocr/static

Then put all .py file to /tmp/ocr

    cp ~/Share/tesseract-web-service/* /tmp/ocr

The default listening port is 1688. Change it in tesseractserver.py to yours.
Please make sure that the firewall is opened for lisenting port.

Start tesseract-web-service by:

    python /tmp/ocr/tesseractserver.py 
    
####How to call RESTful API by tesseract client
tesseractclient.py is an client for calling API.

Type the following command to check the options.

    python /tmp/ocr/tesseractclient.py --help
    
    Usage: tesseractclient.py [options]

    Options:
      -h, --help            show this help message and exit
      -a APIURL, --api-url=APIURL
                            the URL of RESTful tesseract web service
      -i IMAGEURL, --image-url=IMAGEURL
                            the URL of image to do OCR


For example:

    python /tmp/ocr/tesseractclient.py -a "http://localhost:1688/fetchurl" -i "http://price1.suning.cn/webapp/wcs/stores/prdprice/89218_9173_10000_9-1.png"

You should provide the API url and image source url to make it work.

####How to call RESTful API by GET/POST request
The web service provides two HTTP GET pages for testing the API:

    Upload Image File: http://localhost:1688/upload
    Fetch Image From URL: http://localhost:1688/fetchurl

The results are returned in JSON format with ORC result strings.


If you would like the call "Fetch Image From URL" API with POST, please send a HTTP request header similar to the following:

    Connection: keep-alive
    Content-Length: 214
    Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
    Origin: http://localhost:1688
    User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.114 Safari/537.36
    Content-Type: multipart/form-data; boundary=----WebKitFormBoundarylFMK6PAyVCzNCDAr
    Referer: http://localhost:1688/fetchurl
    Accept-Encoding: gzip,deflate,sdch
    Accept-Language: zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4d license
    
    .....
    POST data payload: imageUrl = 'http://xxxxxxx'


If you send POST data by JSON, you need to provide '**url**' key, with the target image url as its value.

Example POST data in JSON:

    {
      'data': {
          'url': 'http://price1.suning.cn/webapp/wcs/stores/prdprice/89218_9173_10000_9-1.png'
      }
    }
    
Then you shall got a JSON response similar to the following:

    {
      'data': {
          'url': 'http://price1.suning.cn/webapp/wcs/stores/prdprice/89218_9173_10000_9-1.png',
          'result': '2158.00'
      }
    }


####Copyright and License

Author: Mark Peng (markpeng.ntu@gmail.com)

All codes are under [the Apache 2.0 license](LICENSE).






    





