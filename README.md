tesseract-web-service
=====================

An implementation of RESTful web service for tesseract-OCR. The HTTP server is implemented using tornado.

As of tesseract-ocr version 3.02.02, it provides a [C-API](https://code.google.com/p/tesseract-ocr/wiki/APIExample).
Now while calling the "Fetch Image From URL" API, all operations are done in memory for better performance. No more file I/O is required. The python implementation of C API wrapper can be found in [**tesseractcapi.py**](https://github.com/guitarmind/tesseract-web-service/blob/master/tesseractcapi.py)

####Support two APIs with GET and POST

    Upload Image File: /upload
    Fetch Image From URL: /fetchurl

####tsseract Installation on Ubuntu 12.04 LTS

    sudo apt-get install python-tornado
    sudo apt-get install python-imaging
    sudo apt-get install tesseract-ocr

Only English letters and digits are supported by default.
You can download more language packs, such as Simplified/Traditional Chinese pack from http://code.google.com/p/tesseract-ocr/downloads/list. 
The packs should be decompressed and put under '**/usr/share/tesseract-ocr/tessdata**'.

    ls /usr/share/tesseract-ocr/tessdata
    
    configs           eng.cube.params        eng.traineddata.__tmp__
    eng.cube.bigrams  eng.cube.size          equ.traineddata
    eng.cube.fold     eng.cube.word-freq     osd.traineddata
    eng.cube.lm       eng.tesseract_cube.nn  tessconfigs
    eng.cube.nn       eng.traineddata

Be sure the set the parent folder path of language packs in environment variables:

    export TESSDATA_PREFIX=/usr/share/tesseract-ocr/


####How to start tesseract-web-service
Create a folder named '**static**' under current folder (for instance, '**/opt/ocr**') to keep temp files

    mkdir /opt/ocr
    mkdir /opt/ocr/static

Then put all .py files to /opt/ocr and make them executable.

    cp ~/Share/tesseract-web-service/* /opt/ocr
    sudo chmod 755 /opt/ocr/*.py

Start tesseract-web-service by:

    python tesseractserver.py -b "/home/markpeng/local/lib" -d "/usr/share/tesseract-ocr/"

Type the following command to check the options.

    python tesseractserver.py -h

    Usage: tesseractserver.py [options]

    Options:
      -h, --help            show this help message and exit
      -p PORT, --port=PORT  the listening port of RESTful tesseract web service.
                            (default: 1688)
      -l LANG, --lang=LANG  the targe language. (defaut: eng
      -b LIBPATH, --lib-path=LIBPATH
                            the absolute path of tesseract library.
      -d TESSDATA, --tessdata-folder=TESSDATA
                            the absolute path of tessdata folder containing
                            language packs.
             

The default listening port is **1688**. Change it to yours on startup.
Please make sure that the firewall is opened for lisenting port.

For example, you can change the port to 8080 by:

    python /opt/ocr/tesseractserver.py -p 8080 -b "/home/markpeng/local/lib" -d "/usr/share/tesseract-ocr/"

####How to call RESTful API by GET/POST request
The web service provides two HTTP GET pages for testing the API:

    Upload Image File: http://localhost:1688/upload
    Fetch Image From URL: http://localhost:1688/fetchurl

The results are returned in JSON format with ORC result strings.


If you would like to call "Fetch Image From URL" API with POST, please send a HTTP request header similar to the following:

    POST /fetchurl HTTP/1.1
    Host: localhost:1688
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


If you send POST data by JSON, you need to provide a '**url**' key, which contains target image url.

Example POST data in JSON:

    data: {
        'url': 'http://price1.suning.cn/webapp/wcs/stores/prdprice/89218_9173_10000_9-1.png'
    }
    
Then you shall get a JSON response similar to the following:

    data: {
        'url': 'http://price1.suning.cn/webapp/wcs/stores/prdprice/89218_9173_10000_9-1.png',
        'result': '2158.00'
    }


####How to call RESTful API by tesseract client
tesseractclient.py is a client for calling the "Fetch Image From URL" API.

Type the following command to check the options.

    python /opt/ocr/tesseractclient.py --help
    
    Usage: tesseractclient.py [options]

    Options:
      -h, --help            show this help message and exit
      -a APIURL, --api-url=APIURL
                            the URL of RESTful tesseract web service
      -i IMAGEURL, --image-url=IMAGEURL
                            the URL of image to do OCR


For instance:

    python /opt/ocr/tesseractclient.py -a "http://localhost:1688/fetchurl" -i "http://www.greatdreams.com/666-magicsquare.gif"

You should provide the API url and image source url to make it work.

####Copyright and License

Author: Mark Peng (markpeng.ntu at gmail)

All codes are under the [Apache 2.0 license](LICENSE).


