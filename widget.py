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

    def __validateJson(self, input):
        if 'type' in input and 'requestId' in input and 'widgetId' in input and 'owner' in input:
            return True
        else:
            return False

class WidgetList:
    widgets = []
    emptyQueue = False
    def __init__(self, queue):
        self.queue = queue
        self.__getWidgets()

    def __getWidgets(self):
        msgList = self.queue.receive_messages(MaxNumberOfMessages=10, VisibilityTimeout=5)
        logging.info("Polled message list")
        if (len(msgList) > 0):
            self.emptyQueue = False
            for msg in msgList:
                data = json.loads(msg.body)
                if self.__validateJson(data):
                    self.widgets.append(data)
                else:
                    logging.error("Missing required information, widget skipped")
                self.queue.delete_messages(
                    Entries=[
                        {
                            'Id': data['widgetId'],
                            'ReceiptHandle': msg.receipt_handle
                        }
                    ]
                )
                # TODO: Add failure handling
        else:
            self.emptyQueue = True

    def getWidget(self):
        if(len(self.widgets) > 0):
            return self.widgets.pop(0)
        else:
            self.__getWidgets()
            if(self.emptyQueue):
                return None
            else:
                return self.widgets.pop(0)

    def checkKeys(self):
        self.__getKeys()
        if len(self.keys) > 0:
            return True
        else:
            return False

    def __validateJson(self, input):
        if 'type' in input and 'requestId' in input and 'widgetId' in input and 'owner' in input:
            return True
        else:
            return False


