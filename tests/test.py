from processor import getBucket, getDB
import pytest

def test_getBucket():
    assert type(getBucket('cs5260-ghaselden-2')) == 'boto3.resources.factory.s3.Bucket'

def test_getDB():
    assert type(getDB()) == 'boto3.resources.factory.dynamodb.Table'

