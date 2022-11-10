from processor import getBucket, getDB, getSQS
from widget import WidgetList, Bucket
import unittest
import boto3

class TestWidgets(unittest.TestCase):
    def test_BucketgetWidget(self):
        readBucket = getBucket("usu-cs5260-ghaselden-1")
        bucket = Bucket(readBucket)
        with self.assertRaises(Exception):
            bucket.getWidget() #Should raise error because bucket is empty

    def test_BucketemptyBucket(self):
        readBucket = getBucket("usu-cs5260-ghaselden-1")
        bucket = Bucket(readBucket)
        self.assertTrue(bucket.emptyBucket())

    def test_WidgetListEmpty(self):
        queue = getSQS("cs5260-requests")
        widgetList = WidgetList(queue)
        self.assertTrue(widgetList.emptyQueue)
    
if __name__ == '__main__':
    unittest.main()