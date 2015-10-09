__author__ = 'lli'

import argparse
import json
import httplib, urllib
from random import randint

PSV_SCHEMA = ['hbid', 'name', 'street_address', 'supplemental_address', "city", "neighbourhood", "state", "zip",
              "country", "phone", "lat", "long", "image"]

ELASTIC_SEARCH_HOST = "localhost"
ELASTIC_SEARCH_PORT = "9200"
INDEX_NAME = "test"
TYPE_NAME = "venue"

ELASTIC_SEARCH_HOST_URL = "{host}:{port}".format(host=ELASTIC_SEARCH_HOST,port=ELASTIC_SEARCH_PORT)
ELASTIC_SEARCH_POST_URL = "/{index_name}/{type_name}".format(index_name=INDEX_NAME,type_name=TYPE_NAME)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--venue', required=True)
    args = parser.parse_args()
    input_file = open(args.venue)
    lines = input_file.readlines()

    docs_list = []
    for line in lines:
        tokens = line.strip("\n").split("|")
        venue_doc = {
            "hbid": tokens[0],
            "name": tokens[1],
            "address": {
                "street_address": tokens[2],
                "supplemental_address": tokens[3],
                "city": tokens[4],
                "neighbourhood": tokens[5],
                "state": tokens[6],
                "zip": tokens[7],
                "country": tokens[8]
            },
            "coordinates": {
                "latitude": tokens[10],
                "longitude": tokens[11]
            },
            "phone": tokens[9],
            "image": tokens[12]
        }
        data = json.dumps(venue_doc)
        print data
        docs_list.append(venue_doc)
        headers = {"content-type": "application/json"}
        conn = httplib.HTTPConnection(ELASTIC_SEARCH_HOST_URL)
        conn.request("POST", ELASTIC_SEARCH_POST_URL, data, headers)
        response = conn.getresponse()
        print response


if __name__ == '__main__':
    main()