from widget import WidgetList, Bucket
import json
from actions import createWidget, updateWidget, deleteWidget
import time
import boto3
import logging


def processor(rb, w, rq):
    logging.info('Starting processor...')
    readBucket = getBucket(rb)
    writeBucket = getBucket(w)
    queue = getSQS(rq)
    db = getDB()
    bucket = Bucket(readBucket)
    widgetList = WidgetList(queue)
    count = 0

    while(count < 10):
        processQueue = []
        if(not bucket.emptyBucket()):
            processQueue.append(bucket.getWidget())
        elif(not widgetList.emptyQueue):
            processQueue.append(widgetList.getWidget())
        else:
            time.sleep(2)
            logging.info('No keys found')
            count += 1
            continue
        for widget in processQueue:
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

def getBucket(name):
    s3 = boto3.resource('s3')
    logging.info(f'Connected to bucket {name}')
    return s3.Bucket(name)

def getDB():
    dynamo = boto3.resource('dynamodb')
    logging.info('Connected to DynamoDB')
    return dynamo.Table('widgets')

def getSQS(name):
    sqs = boto3.resource('sqs')
    url = boto3.client('sqs').get_queue_url(QueueName=name)['QueueUrl']
    logging.info("Connected to SQS")
    return sqs.Queue(url)
