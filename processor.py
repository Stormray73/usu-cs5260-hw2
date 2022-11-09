from widget import WidgetList, Bucket
import json
from actions import createWidget, updateWidget, deleteWidget
import time
import boto3
import logging


def processor(r, w):
    logging.info('Starting processor...')
    readBucket = getBucket(r)
    writeBucket = getBucket(w)
    db = getDB()
    bucket = Bucket(readBucket)
    count = 0
    while(count < 10):
        if(not bucket.emptyBucket()):
            widget = bucket.getWidget()
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

def getBucket(name):
    s3 = boto3.resource('s3')
    logging.info(f'Connected to bucket {name}')
    return s3.Bucket(name)

def getDB():
    dynamo = boto3.resource('dynamodb')
    logging.info('Connected to DynamoDB')
    return dynamo.Table('widgets')

