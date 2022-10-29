import logging
import json

def createWidget(widget, writeBucket, db):
    
    logging.info('Moving to destination bucket...')
    owner = widget['owner']
    owner.replace(" ", "-")
    id = widget['widgetId']
    writeBucket.put_object(Key=f'widgets/{owner}/{id}', Body=json.dumps(widget))
    logging.info('Putting data in DynamoDB...')
    formattedWidget = formatWidget(widget)
    db.put_item(Item=formattedWidget)

def updateWidget(widget, writeBucket, db):
    logging.info("Update request received")

def deleteWidget(widget, writeBucket, db):
    logging.info("Delete request received")


def formatWidget(widget):
    if 'otherAttributes' in widget:
        attributesList = widget.pop('otherAttributes')
        for dict in attributesList:
            widget[dict['name']] = dict['value']
    return widget