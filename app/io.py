from pyjamas import Window
from pyjamas.HTTPRequest import HTTPRequest

from app.json import dumps, loads


class SlideListLoader:
    def __init__(self,after):
        self.after=after

    def onCompletion(self, text):
        self.after(loads(text))

file = "http://api.myjson.com/bins/iqorv"

def apos(x):
    Window.alert(x)

def get_request(after, file_name=file):
    handler=SlideListLoader(after)
    HTTPRequest().asyncGet(file_name, handler)


def put_request(content, file_name=file):
    HTTPRequest().asyncPut(file_name, dumps(content),
                           SlideListLoader(apos), headers={'Content-Type': 'application/json'})


def post_request(content):
    HTTPRequest().asyncPost("http://api.myjson.com/bins/", dumps(content), SlideListLoader(apos),
                            headers={'Content-Type': 'application/json'})
