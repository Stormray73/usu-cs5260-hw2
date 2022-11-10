import logging
import json

def createWidget(widget, writeBucket, db):
    
    logging.info('Create Request Received')
    owner = widget['owner']
    owner.replace(" ", "-")
    id = widget['widgetId']
    writeBucket.put_object(Key=f'widgets/{owner}/{id}', Body=json.dumps(widget))
    logging.info('Putting data in DynamoDB...')
    formattedWidget = formatWidget(widget)
    db.put_item(Item=formattedWidget)

def updateWidget(widget, writeBucket, db):
    logging.info("Update request received")
    owner = widget['owner']
    owner.replace(" ", "-")
    id = widget['widgetId']
    writeBucket.put_object(Key=f'widgets/{owner}/{id}', Body=json.dumps(widget))
    formattedWidget = formatWidget(widget)
    db.put_item(Item=formattedWidget)

def deleteWidget(widget, writeBucket, db):
    logging.info("Delete request received")
    owner = widget['owner']
    owner.replace(" ", "-")
    id = widget['widgetId']
    writeBucket.delete_objects(
        Delete={
            'Objects': [
                {
                    'Key': f'widgets/{owner}/{id}'
                },
            ],
        }
    )
    db.delete_item(
        Key={
            'widgetId': id
        }
    )


def formatWidget(widget):
    if 'otherAttributes' in widget:
        attributesList = widget.pop('otherAttributes')
        for dict in attributesList:
            widget[dict['name']] = dict['value']
    return widget