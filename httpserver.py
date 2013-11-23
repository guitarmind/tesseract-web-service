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
 
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('</pre>'+
                    '<form action="/" method="post" enctype="multipart/form-data">'+
                    '<input type="file" name="the_file" />'+
                    '<input type="submit" value="Submit" />'+'</form>'+
                    '<pre class="prettyprint">')
 
    def post(self):
        self.set_header("Content-Type", "text/html")
        self.write("") # create a unique ID file
        tempname = str(uuid.uuid4()) + ".png"
        myimg = Image.open(StringIO.StringIO(self.request.files.items()[0][1][0]['body']))
        myfilename = os.path.join(os.path.dirname(__file__),"static",tempname);
 
        # save image to file as PNG
        myimg.save(myfilename)
 
        # do OCR, print result
        self.write(image_to_string(myimg))
        self.write("")
 
settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
}
 
application = tornado.web.Application([
    (r"/", MainHandler),
], **settings)
 
if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8080)
    tornado.ioloop.IOLoop.instance().start()

