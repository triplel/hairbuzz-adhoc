__author__ = 'lli'

import argparse
import json
import pymongo
from pymongo import MongoClient
import ast
# import create_collections

VENUE_PSV_SCHEMA = ['hbid', 'name', 'street_address', 'supplemental_address', 'city', 'neighbourhood', 'state', 'zip',
                    'country', 'phone', 'latitude', 'longitude', 'image']


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--venue', required=True)
    args = parser.parse_args()
    venues_file = open(args.venue)
    venue_list = []
    for line in venues_file:
        tokens = line.lower().strip("\r").strip("\n").split("|")
        venue_doc = {
            "venue_hbid": tokens[0],
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
            "venue_coordinates": {
                "venue_latitude": float(tokens[10]),
                "venue_longitude": float(tokens[11])
            },
            "phone": tokens[9],
            "image": tokens[12]
        }
        # print venue_doc
        venue_list.append(venue_doc)

    client = MongoClient('localhost', 27017)
    hb_dev = client.dev
    # print cip_test.collection_names()

    venues_collection = hb_dev.venues
    # clean up the collection before reinserting
    venues_collection.remove()

    venues_collection.ensure_index([("name", 1), ("phone", 1)], unique=True)

    venues_collection.insert(venue_list)
    print "{count} venues inserted in venues collection".format(count=venues_collection.count())


if __name__ == '__main__':
    main()