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
    db = getDB()
    widgetList = WidgetList(readBucket)
    count = 0
    while(count < 10):
        if(widgetList.checkKeys()):
            widget = getWidget(readBucket, widgetList)
            if widget is None:
                continue
            if (widget['type'] == 'create'):
                createWidget(widget, writeBucket, db)
            elif(widget['type'] =='update'):
                updateWidget(widget, writeBucket, db)
            elif(widget['type'] == 'delete'):
                deleteWidget(widget, writeBucket, db)
            else:
                logging.warning("Invalid action type for widget with ID: " + widget['widgetId'])
        else:
            time.sleep(.1)
            logging.info('No keys found in S3 Bucket')
            count += 1

def getWidget(readBucket, widgetList):
    nextKey = widgetList.getNextKey()
    widgetDict = getWidgetJson(readBucket, nextKey)
    return widgetDict

def getWidgetJson(readBucket, fileName):
    readBucket.download_file(fileName, fileName)
    f = open(fileName)
    data = None
    try:
        data = json.load(f)
        if not validateJson(data):
            logging.warning('Missing required data, skipping file')
            data = None
    except Exception as ex:
        logging.warning("Error converting to JSON, skipping file: " + str(ex))
    finally:
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

def validateJson(input):
    if 'type' in input and 'requestId' in input and 'widgetId' in input and 'owner' in input:
        return True
    else:
        return False