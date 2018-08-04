
import boto3
from urilib import Uri
import pprint
import textwrap


class DottedDict:

    def __init__(self,response,level=0):
        self._level =level
        self._data = response
        self._tree= {}
        for k in response.keys() :
            if type(response[k]) == type({"a" : "dict"}) :
                self._tree.update({k: DottedDict(response[k], level+1)})
            else :
                self._tree.update({k : response[k]})




    def show(self):
        DottedDict.printTree(self._data)

    @staticmethod
    def printTree(tree, depth=0):
        if tree == None or len(tree) == 0:
            print "\t" * depth, "-"
        else:
            if type(tree) == type({"a" : "dict"}):
                for key, val in tree.items():
                    print " "*depth+"|"
                    print " " * depth+"+---", key
                    DottedDict.printTree(val, depth + 1)
            else :
                print " " * depth+"   |"
                print " " * depth+"   +---", str(tree)


    def keys(self):
        return self._tree.keys()

    def __repr__(self):
        return str(self._data)


    def __getitem__(self, item):
        return self._data[item]

if __name__ == "__main__" :
    data = {
        "Environment" : {
            "tests" : {
                "globals" : {
                    "AWSAccountId" : "xxx"
                },
                "platforms" : {
                    "uri:platform:123456:dev": {
                        "foo" : "bar"
                    }
                }
            }
        }
    }
    d = DottedDict(data)
    d.show()



