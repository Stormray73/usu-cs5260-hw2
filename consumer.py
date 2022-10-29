
from datetime import datetime
import logging
import argparse

from processor import processor

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', action='store', type=str, required=True)
    parser.add_argument('-w', action='store', type=str, required=True)
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO)
    logging.info("parsing arguments...")
    processor(args.r, args.w)



    