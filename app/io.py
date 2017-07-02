from pyjamas import Window
from pyjamas.HTTPRequest import HTTPRequest

from app.json import dumps, loads


class SlideListLoader:
    def __init__(self):
        pass

    def onCompletion(self, text):
        Window.alert("done")

    def onError(self, text, code):
        Window.alert("error: " + text + " " + code)

    def onTimeout(self, text):
        Window.alert("timeout")


file = "http://api.myjson.com/bins/iqorv"


def get_request(handler=SlideListLoader(), file_name=file):
    HTTPRequest().asyncGet(file_name, handler)


def put_request(content, file_name=file):
    HTTPRequest().asyncPut(file_name, dumps(content),
                           SlideListLoader(), headers={'Content-Type': 'application/json'})


def post_request(content):
    HTTPRequest().asyncPost("http://api.myjson.com/bins/", dumps(content), SlideListLoader(),
                            headers={'Content-Type': 'application/json'})
