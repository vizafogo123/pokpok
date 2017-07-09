from pyjamas import Window
from pyjamas.HTTPRequest import HTTPRequest

from app.json import dumps, loads
from lion.Operation import Operation
from lion.Theorem import Theorem


class SlideListLoader:
    def __init__(self,after):
        self.after=after

    def onCompletion(self, text):
        self.after(loads(text))

file_name = "http://api.myjson.com/bins/iqorv"

class IO:


    @staticmethod
    def apos(x):
        Window.alert("saved")

    @staticmethod
    def get_request(after, file_name=file_name):
        handler=SlideListLoader(after)
        HTTPRequest().asyncGet(file_name, handler)


    @staticmethod
    def put_request(content, file_name=file_name):
        HTTPRequest().asyncPut(file_name, dumps(content),
                               SlideListLoader(IO.apos), headers={'Content-Type': 'application/json'})


    @staticmethod
    def post_request(content):
        HTTPRequest().asyncPost("http://api.myjson.com/bins/", dumps(content), SlideListLoader(IO.apos),
                                headers={'Content-Type': 'application/json'})

    @staticmethod
    def save():
        IO.put_request({"operations": [o.to_json() for o in Operation.global_operations],
                     "theorems": [t.to_json() for t in Theorem.theorems]})
