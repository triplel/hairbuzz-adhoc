__author__ = 'lli'

import argparse
import json
import httplib, urllib
from random import randint
import ast

STYLIST_PSV_SCHEMA = ['hbid', 'first_name', 'last_name', 'gender', 'rating', 'price_rank', 'reviews', 'avatar', 'venue_hbid']

VENUE_PSV_SCHEMA = ['hbid', 'name', 'street_address', 'supplemental_address', 'city', 'neighbourhood', 'state', 'zip',
                    'country', 'phone', 'latitude', 'longitude', 'image']


ODDITY_SCHEMA = ['id', 'biz_name', 'biz_info', 'cat_primary', 'cat_sub', 'e_address', 'e_city', 'e_state', 'e_postal',
                 'e_zip_full', 'e_country', 'loc_county', 'loc_area_code', 'loc_FIPS', 'loc_MSA', 'loc_PMSA', 'loc_TZ', 'loc_DST',
                 'loc_LAT_centroid', 'loc_LAT_poly', 'loc_LONG_centroid', 'loc_LONG_poly', 'biz_phone', 'biz_phone_ext', 'biz_fax', 'biz_email', 'web_url',
                 'web_meta_title', 'web_meta_desc', 'web_meta_keys']


ELASTIC_SEARCH_HOST = "localhost"
ELASTIC_SEARCH_PORT = "9200"
INDEX_NAME = "test"
TYPE_NAME = "stylist"

ELASTIC_SEARCH_HOST_URL = "{host}:{port}".format(host=ELASTIC_SEARCH_HOST,port=ELASTIC_SEARCH_PORT)
ELASTIC_SEARCH_POST_URL = "/{index_name}/{type_name}".format(index_name=INDEX_NAME,type_name=TYPE_NAME)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--stylist', required=True)
    parser.add_argument('--venue', required=True)
    args = parser.parse_args()
    stylists_file = open(args.stylist)
    venues_file = open(args.venue)
    # stylists = stylists_file.readlines()

    venue_map = {}
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
                "venue_latitude": tokens[10],
                "venue_longitude": tokens[11]
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
            "rating": tokens[4],
            "price_rank": tokens[5],
            "reviews": tokens[6],
            "work_place": ast.literal_eval(venue_map[tokens[8].strip("\r")])
        }
        data = json.dumps(stylist_doc)
        print data
        headers = {"content-type": "application/json"}
        conn = httplib.HTTPConnection(ELASTIC_SEARCH_HOST_URL)
        conn.request("POST", ELASTIC_SEARCH_POST_URL, data, headers)
        response = conn.getresponse()
        print response


if __name__ == '__main__':
    main()