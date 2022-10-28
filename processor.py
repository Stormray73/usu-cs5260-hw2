from fileinput import filename
from widget import WidgetList, decoder
import json
from actions import createWidget, updateWidget, deleteWidget
import time

def processor(readBucket, writeBucket):
    widgetList = WidgetList(readBucket)
    while(True):
        if(widgetList.checkKeys()):
            widget = getWidget(readBucket, widgetList)
            if (widget.type == 'WidgetCreateRequest'):
                createWidget(widget, writeBucket)
            elif(widget.type =='WidgetUpdateRequest'):
                updateWidget(widget, writeBucket)
            elif(widget.type == 'WidgetDeleteRequest'):
                deleteWidget(widget, writeBucket)
            #else - throw warning error
        else:
            time.sleep(.1)

def getWidget(readBucket, widgetList):
    nextKey = widgetList.getNextKey()
    widgetDict = getWidgetJson(readBucket, nextKey)
    return decoder(widgetDict)

def getWidgetJson(readBucket, fileName):
    readBucket.download_file(fileName, f'/tmp/{fileName}')
    f = open(fileName)
    data = json.load(f)
    f.close()
    return data
