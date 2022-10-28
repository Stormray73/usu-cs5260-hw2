import re
import boto3
import logging
import argparse

def getBucket(name):
    s3 = boto3.resource('s3')
    return s3.Bucket(name)
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', action='store', type=str, required=True)
    parser.add_argument('-w', action='store', type=str, required=True)
    args = parser.parse_args()

    readBucket = getBucket(args.r)
    writeBucket = getBucket(args.w)
    
    


    