#!/usr/bin/env python
import sys
import optparse
import tornado.httpclient
import simplejson, json
import urllib

"""
Get result string from tesseract API
"""
def ocrAPI(apiUrl, imageUrl):
    request = { 'url': imageUrl }
    jsonstr = { 'data': request }
    post_data = json.dumps(jsonstr)

    headers = { 'Content-Type': 'application/json; charset=UTF-8' }
    http_client = tornado.httpclient.AsyncHTTPClient()
    http_client.fetch(apiUrl, handle_request, method = 'POST', headers = headers, body = post_data)
    print "Sending request: " + post_data
    tornado.ioloop.IOLoop.instance().start()

def handle_request(response):
    if response.error:
        print "Error: ", response.error
    else:
        print "Got response: " + response.body

def main():
    parser = optparse.OptionParser()
    parser.add_option('-a', '--api-url', dest='apiUrl', help='the URL of RESTful tesseract web service')
    parser.add_option('-i', '--image-url', dest='imageUrl', help='the URL of image to do OCR')
    (options, args) = parser.parse_args()

    if not options.apiUrl:   # if apiUrl is not given
      parser.error('api-url not given')
    if not options.imageUrl:   # if imageUrl is not given
      parser.error('image-url not given')

    #apiUrl = "http://localhost:1688/fetchurl";
    #imageUrl = "http://price1.suning.cn/webapp/wcs/stores/prdprice/89218_9173_10000_9-1.png"

    # call tesseract API
    ocrAPI(options.apiUrl, options.imageUrl)
 
if __name__ == '__main__':
    main()
