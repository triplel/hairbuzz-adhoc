__author__ = 'lli'

import argparse
import json
import pymongo
from pymongo import MongoClient
import ast


STYLIST_PSV_SCHEMA = ['hbid', 'first_name', 'last_name', 'gender', 'rating', 'price_rank', 'reviews', 'avatar', 'venue_hbid']
VENUE_PSV_SCHEMA = ['hbid', 'name', 'street_address', 'supplemental_address', 'city', 'neighbourhood', 'state', 'zip',
                    'country', 'phone', 'latitude', 'longitude', 'image']


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--stylist', required=True)
    parser.add_argument('--venue', required=True)
    args = parser.parse_args()
    stylists_file = open(args.stylist)
    venues_file = open(args.venue)

    venue_map = {}
    stylist_josn_list = []

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
        data = json.dumps(venue_doc)
        venue_map[venue_doc["venue_hbid"]] = data

    for line in stylists_file:
        tokens = line.lower().strip("\r").strip("\n").split("|")
        stylist_doc = {
            "hbid": tokens[0],
            "first_name": tokens[1],
            "last_name": tokens[2],
            "slug": "",
            "avatar": tokens[7],
            "gender": tokens[3],
            "rating": int(tokens[4]),
            "price_rank": int(tokens[5]),
            "reviews": int(tokens[6]),
            "work_place": ast.literal_eval(venue_map[tokens[8].strip("\r")])
        }
        # print stylist_doc
        stylist_josn_list.append(stylist_doc)

    client = MongoClient('localhost', 27017)
    hb_dev = client.dev
    # print cip_test.collection_names()

    stylists_collection = hb_dev.stylists
    # clean up the collection before reinserting
    stylists_collection.drop()
    stylists_collection.insert(stylist_josn_list)
    print "{count} stylists inserted in stylists collection".format(count=stylists_collection.count())


if __name__ == '__main__':
    main()