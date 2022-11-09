import json
from collections import namedtuple
import logging
import os

class Bucket:
    def __init__(self, readBucket):
        self.__readBucket = readBucket

    def emptyBucket(self):
        keys = self.__getKeyList()
        if len(keys) == 0:
            return True
        else:
            return False

    def __getKeyList(self):
        keys = []
        for obj in self.__readBucket.objects.all():
            keys.append(obj.key)
        return keys

    def __getNextKey(self):
        keys = self.__getKeyList()
        keys.sort()
        return keys.pop(0)

    def getWidget(self):
        filename = self.__getNextKey()
        self.__readBucket.download_file(filename, filename)
        f = open(filename)
        data = None
        try:
            data = json.load(f)
            if not self.__validateJson(data):
                logging.warning('Missing required data, skipping file')
                data = None
        except Exception as ex:
            logging.warning("Error converting to JSON, skipping file: " + str(ex))
        finally:
            f.close()
            os.remove(filename)
            self.__readBucket.delete_objects(
                Delete={
                    'Objects': [
                        {
                            'Key': filename
                        },
                    ],
                }
            )
        return data

    def __validateJson(input):
        if 'type' in input and 'requestId' in input and 'widgetId' in input and 'owner' in input:
            return True
        else:
            return False

class WidgetList:
    keys = []
    def __init__(self, readBucket):
        self.readBucket = readBucket
        self.__getKeys()

    def __getKeys(self):
        logging.info('Getting keys from producer...')
        for obj in self.readBucket.objects.all():
            if obj.key not in self.keys:
                self.keys.append(obj.key)

    def getNextKey(self):
        self.__getKeys()

        self.keys.sort()
        return self.keys.pop(0)

    def checkKeys(self):
        self.__getKeys()
        if len(self.keys) > 0:
            return True
        else:
            return False


