
from datetime import datetime
import logging
import argparse
import sys

from processor import processor

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-rb', action='store', type=str, required=False)
    parser.add_argument('-rq', action='store', type=str, required=False)
    parser.add_argument('-w', action='store', type=str, required=True)
    args = parser.parse_args()
    fname = datetime.now().strftime("%Y-%m-%d-%H-%M")
    logging.basicConfig(filename=f'{fname}.log',level=logging.INFO)
    logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
    logging.info("parsing arguments...")
    if args.rb == None and args.rq == None:
        logging.error("Invalid args, must have at least a read bucket or a read queue")
    else:
        processor(args.rb, args.w, args.rq)
    logging.info("Programme Terminating...")



    