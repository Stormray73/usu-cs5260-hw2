import re
import boto3
import logging
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', action='store', type=str, required=True)
    parser.add_argument('-w', action='store', type=str, required=True)
    args = parser.parse_args()

    