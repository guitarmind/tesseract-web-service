#!/usr/bin/env python
import tornado.httpserver
import tornado.ioloop
import tornado.web
import pprint
import Image
from tesseractapi import image_to_string
import StringIO
import os.path
import uuid

# for downloading PNG image from url
import urllib, cStringIO
import json

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
        tmpFilename = os.path.join(os.path.dirname(__file__), "static", tempname)
 
        # do OCR, print result
        result = image_to_string(tmpImg).replace(" ", "")
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
                        $("input#submitBtn").submit(function() {
                            var imageUrl = document.getElementById("imageUrl").value;
                            var resultEle = document.getElementById("result");


                            alert('123');

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
                    <h2>Tesseract Web Service &nbsp;by Mark Peng (markpeng.ntu@gmail.com)</h2>
                    <form name="mainForm" id="mainForm" action="" method="POST" enctype="multipart/form-data">
                        Target image url: <input type="text" id="imageUrl" name="imageUrl" size="50" />
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
            url = jsonobj['data']['url']

        # temp image folder
        dir = "/tmp/ocr/static/"

        # download image from url
        file = cStringIO.StringIO(urllib.urlopen(url).read())
        tmpImg = Image.open(file)
 
        # do OCR, get result string
        result = image_to_string(tmpImg).replace(" ", "")

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
 
if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(1688)
    tornado.ioloop.IOLoop.instance().start()

