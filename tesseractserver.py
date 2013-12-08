#!/usr/bin/env python
import tornado.httpserver
import tornado.ioloop
import tornado.web
import optparse
import pprint
import Image
from tesseractapi import image_to_string
import StringIO
import os.path
import uuid

# for downloading PNG image from url
import urllib, cStringIO
import json

# C API wrapper
from tesseractcapi import tesseactWrapper

# global variables
lang = "eng"
libpath = ""
tessdata = ""

"""
Handles the GET/POST of image files to OCR result string.
"""
class FileUploadHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('</pre>'+
                    '<form action="/upload" method="post" enctype="multipart/form-data">'+
                    '<input type="file" name="the_file" />'+
                    '<input type="submit" value="Submit" />'+'</form>'+
                    '<pre class="prettyprint">')
 
    def post(self):
        self.set_header("Content-Type", "text/html")
        self.write("") 
        # create a unique ID file
        tempname = str(uuid.uuid4()) + ".png"
        tmpImg = Image.open(StringIO.StringIO(self.request.files.items()[0][1][0]['body']))
        
        # force resize to width=150px if the incoming image is too small
        targetWidth = 150
        width, height = tmpImg.size
        if width < targetWidth:
            ratio = float(targetWidth) / width
            newHeight = int(height * ratio)
            tmpImg = tmpImg.resize((targetWidth, newHeight), Image.ANTIALIAS)
            print "resize image to (" + str(targetWidth) + "," + str(newHeight) + ")"

        # do OCR, print result
        result = image_to_string(tmpImg)
        if "." not in result and " " in result:
            result = result.replace(" ", ".")
        else:
            result = result.replace(" ", "")
        self.write(result)
        self.write("")


"""
Handles the GET/POST of image url to OCR result string.
"""
class ImageUrlHandler(tornado.web.RequestHandler):
    def initialize(self, *args, **kwargs):
        self.contentType = self.request.headers.get('Content-Type')

    def get(self):
        html = """
                <html>
                <title>Tesseract Web Service</title>
                <script src="//ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js"></script> 
                <script>
                    $(document).ready(function(){
                        $("form#mainForm").submit(function() {
                            var imageUrl = document.getElementById("imageUrl").value;
                            var resultEle = document.getElementById("result");

                            if(imageUrl !== "") {
                                $.ajax({
                                       type: "POST",
                                       url: "/fetchurl",
                                       contentType: 'multipart/form-data',
                                       data: $('form#mainForm').serialize(),
                                       success: function(data) {
                                           alert('data:' + data);
                                           resultEle.innerHTML = "<span>Result JSON:</span><br/>" + data;
                                       }
                                });
                            }

                            return false; // avoid to execute the actual submit of the form.
                        });
                    });  
                </script>
                <body>
                    <h2>Tesseract Web Service</h2>
                    <form name="mainForm" id="mainForm" action="" method="POST" enctype="multipart/form-data">
                        Target image url: <input type="text" id="imageUrl" name="imageUrl" size="80" />
                        <input id="submitBtn" type="submit" value="Submit" />
                    </form>
                    <div id="result"></div>
                </body>
                </html>
               """
        self.write(html)

    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")

        if("multipart/form-data" in self.contentType):
            url = self.get_argument("imageUrl", default = None, strip = False)
        else:
            # parse received json
            jsonobj = json.loads(self.request.body)
            jsonobj['url']
            # url = jsonobj['data']['url']

        # force resize to width=150px if the incoming image is too small for better precision
        minWidth = 150;
 
        # do OCR, get result string
        wrapper = tesseactWrapper(lang, libpath, tessdata)
        result = wrapper.imageUrlToString(url, minWidth)
        if "." not in result and " " in result:
            result = result.replace(" ", ".")
        else:
            result = result.replace(" ", "")

        # send response json
        response = { 'result': result, 'url': url }
        self.write(response)

        print response

 
settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
}
 
application = tornado.web.Application([
    (r"/upload", FileUploadHandler),
    (r"/fetchurl", ImageUrlHandler)
], **settings)

def main():
    parser = optparse.OptionParser()
    parser.add_option('-p', '--port', dest='port', help='the listening port of RESTful tesseract web service. (default: 1688)')
    parser.add_option('-l', '--lang', dest='lang', help='the targe language. (defaut: eng')
    parser.add_option('-b', '--lib-path', dest='libPath', help='the absolute path of tesseract library.')
    parser.add_option('-d', '--tessdata-folder', dest='tessdata', help='the absolute path of tessdata folder containing language packs.')
    (options, args) = parser.parse_args()

    global lang
    global libpath
    global tessdata

    if options.lang:   # if lang is given
        lang = options.lang
    if not options.libPath:   # if libPath is not given
        parser.error('lib-path not given')
    else:
        libpath = options.libPath
    if not options.tessdata:   # if tessdata is not given
        parser.error('tessdata not given')
    else:
        tessdata = options.tessdata

    port = options.port
    if not options.port:   # if port is not given, use the default one 
        port = 1688

    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(port)
    print "Tesseract Web Service starts at port " + str(port) + "."
    tornado.ioloop.IOLoop.instance().start()
 
if __name__ == "__main__":
    main()

