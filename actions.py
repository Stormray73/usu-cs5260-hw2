import logging

def createWidget(widget, writeBucket, db):
    logging.info('Putting data in DynamoDB...')
    db.put_item(widget)
    logging.info('Moving to destination bucket...')
    writeBucket.put_object(widget)

def updateWidget(widget, writeBucket, db):
    pass

def deleteWidget(widget, writeBucket, db):
    pass


