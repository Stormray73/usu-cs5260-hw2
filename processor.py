from fileinput import filename
import imp
from widget import WidgetList, decoder
import json
from actions import createWidget, updateWidget, deleteWidget
import time
import boto3
import logging
import os

def processor(r, w):
    logging.info('Starting processor...')
    readBucket = getBucket(r)
    writeBucket = getBucket(w)
    widgetList = WidgetList(readBucket)
    while(True):
        if(widgetList.checkKeys()):
            widget = getWidget(readBucket, widgetList)
            if (widget['type'] == 'WidgetCreateRequest'):
                createWidget(widget, writeBucket, getDB())
            elif(widget['type'] =='WidgetUpdateRequest'):
                updateWidget(widget, writeBucket, getDB())
            elif(widget['type'] == 'WidgetDeleteRequest'):
                deleteWidget(widget, writeBucket, getDB())
            #else - throw warning error
        else:
            time.sleep(.1)

def getWidget(readBucket, widgetList):
    nextKey = widgetList.getNextKey()
    widgetDict = getWidgetJson(readBucket, nextKey)
    return widgetDict

def getWidgetJson(readBucket, fileName):
    readBucket.download_file(fileName, fileName)
    f = open(fileName)
    data = json.load(f)
    f.close()
    os.remove(fileName)
    readBucket.delete_objects(
        Delete={
            'Objects': [
                {
                    'Key': fileName
                },
            ],
        }
    )
    return data

def getBucket(name):
    s3 = boto3.resource('s3')
    logging.info(f'Connected to bucket {name}')
    return s3.Bucket(name)

def getDB():
    dynamo = boto3.resource('dynamodb')
    logging.info('Connected to DynamoDB')
    return dynamo.Table('widgets')