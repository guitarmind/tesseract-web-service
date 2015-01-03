tesseract-web-service
=====================

An implementation of RESTful web service for tesseract-OCR. The HTTP server is implemented using tornado. A [**Docker Container**](https://registry.hub.docker.com/u/guitarmind/tesseract-web-service/) has been created to let you run this service without any installation efforts!

As of tesseract-ocr version 3.02.02, it provides a [C-API](https://code.google.com/p/tesseract-ocr/wiki/APIExample).
Now while calling the "Fetch Image From URL" API, operations are done in memory for better performance. No file I/O is required. The python implementation of C API wrapper using ctypes can be found in [**tesseractcapi.py**](https://github.com/guitarmind/tesseract-web-service/blob/master/tesseractcapi.py). Bulk processing is planned to appear in the future version.

A full list of C APIs supported in tesseract-ocr version 3.02.02 is at [here](https://code.google.com/p/tesseract-ocr/source/browse/api/capi.h) with detailed signatures and comments.


####Support two APIs with GET and POST

    Upload Image File: /upload
    Fetch Image From URL: /fetchurl


####Tesseract Installation on Ubuntu 12.04 LTS

Python Requirement

    version >= 2.7

Install tornado, PIL image library and other required packages by apt-get.

    sudo apt-get update && sudo apt-get install -y \
        autoconf \
        automake \
        autotools-dev \
        build-essential \
        checkinstall \
        libjpeg-dev \
        libpng-dev \
        libtiff-dev \
        libtool \
        python \
        python-imaging \
        python-tornado \
        wget \
        zlib1g-dev
    
You need to compile and install leptonica and the latest version (3.02.02) of tesseract-ocr manually to support C API. More details can be found at [this wiki](https://code.google.com/p/tesseract-ocr/wiki/Compiling). Here is an example on Ubuntu 12.04 LTS:

    mkdir ~/temp \
        && cd ~/temp/ \
        wget http://www.leptonica.org/source/leptonica-1.69.tar.gz \
        && tar -zxvf leptonica-1.69.tar.gz \
        && cd leptonica-1.69 \
        && ./configure \
        && make \
        && checkinstall \
        && ldconfig


    cd ~/temp/ \
        && wget https://tesseract-ocr.googlecode.com/files/tesseract-ocr-3.02.02.tar.gz \
        && tar xvf tesseract-ocr-3.02.02.tar.gz \
        && cd tesseract-ocr \
        && ./autogen.sh \
        && mkdir ~/local \
        && ./configure --prefix=$HOME/local/ \
        && make \
        && make install

Only English letters and digits are supported by default.
You can download more language packs, such as Simplified/Traditional Chinese pack from http://code.google.com/p/tesseract-ocr/downloads/list. 
Decompress and put the packs under '**~/local/share/**' or other locations you like.

    cd ~/local/share \
        && wget https://tesseract-ocr.googlecode.com/files/tesseract-ocr-3.02.eng.tar.gz \
        && tar xvf tesseract-ocr-3.02.eng.tar.gz

    ls ~/local/share/tesseract-ocr/tessdata
    
    configs           eng.cube.params        eng.traineddata.__tmp__
    eng.cube.bigrams  eng.cube.size          equ.traineddata
    eng.cube.fold     eng.cube.word-freq     osd.traineddata
    eng.cube.lm       eng.tesseract_cube.nn  tessconfigs
    eng.cube.nn       eng.traineddata

Be sure to set the parent folder path of language packs in environment variables, for instance:

    export TESSDATA_PREFIX=/home/markpeng/local/share/tesseract-ocr/



####How to start tesseract-web-service
Create a folder named '**static**' under current folder (for instance, '**/opt/ocr**') to keep temp files

    sudo mkdir /opt/ocr
    sudo mkdir /opt/ocr/static

Then put all .py files to /opt/ocr and make them executable.

    sudo cp ~/Share/tesseract-web-service/* /opt/ocr
    sudo chmod 755 /opt/ocr/*.py

Note: you should go to the folder path containing the **static** folder to make the service work.

    cd /opt/ocr

Now, start tesseract-web-service by:

    python tesseractserver.py -b "/home/markpeng/local/lib" -d "/home/markpeng/local/share/tesseract-ocr"

Type the following command to check the options.

    python tesseractserver.py -h

    Usage: tesseractserver.py [options]

    Options:
      -h, --help            show this help message and exit
      -p PORT, --port=PORT  the listening port of RESTful tesseract web service.
                            (default: 1688)
      -l LANG, --lang=LANG  the targe language. (default: eng)
      -b LIBPATH, --lib-path=LIBPATH
                            the absolute path of tesseract library.
      -d TESSDATA, --tessdata-folder=TESSDATA
                            the absolute path of tessdata folder containing
                            language packs.
             

The default listening port is **1688**. Change it to yours on startup.
Please make sure that the firewall is opened for listening port.

For example, you can change the port to 8080 by:

    python /opt/ocr/tesseractserver.py -p 8080 -b "/home/markpeng/local/lib" -d "/home/markpeng/local/share/tesseract-ocr"

To start it as a persistent service even after terminal logout:

    sudo nohup python /opt/ocr/tesseractserver.py -p 8080 -b "/home/markpeng/local/lib" -d "/home/markpeng/local/share/tesseract-ocr" &

####How to call RESTful API by GET/POST request
The web service provides two HTTP GET pages for testing the API:

    Upload Image File: http://localhost:1688/upload
    Fetch Image From URL: http://localhost:1688/fetchurl

The results are returned in JSON format with OCR result strings.


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


####How to pull and run Docker Container
Install Docker to your host by following the [official installation guide](https://docs.docker.com/installation/#installation).

After that, execute the following command to download Docker Image (packaged in Ubuntu 12.04 LTS):

    docker pull guitarmind/tesseract-web-service

To run the web service using container, just type:

    docker run --rm -d -p 1688:1688 guitarmind/tesseract-web-service

Note that the -p flag is used to bind local port with Container's virtual port. By default it is set to 1688. You can change it by modifying the [Dockerfile](https://github.com/guitarmind/tesseract-web-service/blob/master/Dockerfile). The -d flag means to run it in daemon mode.

The container has been created as an Automated Build:

https://registry.hub.docker.com/u/guitarmind/tesseract-web-service/

##Changelog

####0.0.1 - 2013-11-23

Features:

  - Support basic GET/POST APIs for "upload" and "fetchUrl" APIs
  - File-based processing


####0.0.2 - 2013-12-08

Features:

  - Add a Python wrapper for calling tesseract-ocr C API directly
  - Memory-based processing for "fetchUrl" API


####0.0.3 - 2015-01-03

Features:

  - Add a Docker Container for easy installation and deployment


##Copyright and License

Author: Mark Peng (markpeng.ntu at gmail)

All codes are under the [Apache 2.0 license](LICENSE).


