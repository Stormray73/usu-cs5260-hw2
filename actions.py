import logging
import json

def createWidget(widget, writeBucket, db):
    logging.info('Putting data in DynamoDB...')
    db.put_item(Item=widget)
    logging.info('Moving to destination bucket...')
    owner = widget['owner']
    owner.replace(" ", "-")
    id = widget['widgetId']
    writeBucket.put_object(Key=f'widgets/{owner}/{id}', Body=json.dumps(widget))

def updateWidget(widget, writeBucket, db):
    logging.info("Update request received")

def deleteWidget(widget, writeBucket, db):
    pass


