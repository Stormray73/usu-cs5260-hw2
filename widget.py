import json
from collections import namedtuple
import logging

class Widget:
    
    def __init__(self, wtype, requestId, widgetId, owner, attributes = []):
        self.type = wtype
        self.requestId = requestId
        self.widgetId = widgetId
        self.owner = owner
        self.attributes = attributes

class WidgetList:
    keys = []
    def __init__(self, readBucket):
        self.readBucket = readBucket
        self.getKeys(readBucket)

    def getKeys(self, readBucket):
        logging.info('Getting keys from producer...')
        for obj in readBucket.objects.all():
            if obj.key not in self.keys:
                self.keys.append(obj.key)

    def getNextKey(self):
        self.getKeys(self.readBucket)
        
        self.keys.sort()
        return self.keys.pop(0)

    def checkKeys(self):
        self.getKeys(self.readBucket)
        if len(self.keys) > 0:
            return True
        else:
            return False

def decoder(widgetDict):
    return namedtuple('X', widgetDict.keys())(*widgetDict.values())

