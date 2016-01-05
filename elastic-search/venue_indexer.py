__author__ = 'lli'

import argparse
import json
import httplib, urllib
from random import randint
import venue_helper

PSV_SCHEMA = ['hbid', 'name', 'street_address', 'supplemental_address', "city", "neighbourhood", "state", "zip",
              "country", "phone", "lat", "long", "image"]


ODDITY_SCHEMA = ['id', 'biz_name', 'biz_info', 'cat_primary', 'cat_sub', 'e_address', 'e_city', 'e_state', 'e_postal',
                 'e_zip_full', 'e_country', 'loc_county', 'loc_area_code', 'loc_FIPS', 'loc_MSA', 'loc_PMSA', 'loc_TZ', 'loc_DST',
                 'loc_LAT_centroid', 'loc_LAT_poly', 'loc_LONG_centroid', 'loc_LONG_poly', 'biz_phone', 'biz_phone_ext', 'biz_fax', 'biz_email', 'web_url',
                 'web_meta_title', 'web_meta_desc', 'web_meta_keys']


ELASTIC_SEARCH_HOST = "localhost"
ELASTIC_SEARCH_PORT = "9200"
INDEX_NAME = "test"
TYPE_NAME = "venue"


DEFAULT_VENUE_PICTURE = "https://s3.amazonaws.com/hairbuzz.signup.profile.pics/Studio/salon_inner.jpg"

ELASTIC_SEARCH_HOST_URL = "{host}:{port}".format(host=ELASTIC_SEARCH_HOST,port=ELASTIC_SEARCH_PORT)
ELASTIC_SEARCH_POST_URL = "/{index_name}/{type_name}".format(index_name=INDEX_NAME,type_name=TYPE_NAME)


def build_from_oddity_data(data):
    tokens = data.lower().strip("\n").replace('\"', '').split(",")
    hbid = "V{:010}".format(int(tokens[0]))
    phone = tokens[22].replace(' ', '').replace('(', '').replace(')', '').replace('-', '')
    venue_doc = {
        "hbid": hbid,
        "name": tokens[1],
        "address": {
            "street_address": tokens[5],
            "supplemental_address": "",
            "city": tokens[6],
            "neighbourhood": tokens[11],
            "state": tokens[7],
            "zip": tokens[8],
            "country": tokens[10]
        },
        "coordinates": {
            "latitude": tokens[18],
            "longitude": tokens[20]
        },
        "phone": phone,
        "image": DEFAULT_VENUE_PICTURE
    }
    return venue_doc


def build_from_test_psv(data):
    tokens = data.lower().strip("\n").split("|")
    hbid = "V{:010}".format(int(tokens[0]))
    venue_doc = {
        "hbid": hbid,
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
    return venue_doc


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', help='sources of data', choices=['test', 'oddity'], required=True)
    parser.add_argument('--input', help='source files for venues', required=True)
    args = parser.parse_args()
    input_file = open(args.input)
    source_type = args.source
    lines = input_file.readlines()
    docs_list = []

    if source_type == 'test':
        for line in lines:
            venue_doc = build_from_test_psv(line)
            data = json.dumps(venue_doc)
            print data
            docs_list.append(venue_doc)
            headers = {"content-type": "application/json"}
            conn = httplib.HTTPConnection(ELASTIC_SEARCH_HOST_URL)
            conn.request("POST", ELASTIC_SEARCH_POST_URL, data, headers)
            response = conn.getresponse()
            print response
    else:
        counter = 0
        for line in lines:
            venue_doc = build_from_oddity_data(line)
            data = json.dumps(venue_doc)
            # print data
            docs_list.append(venue_doc)
            headers = {"content-type": "application/json"}
            conn = httplib.HTTPConnection(ELASTIC_SEARCH_HOST_URL)
            conn.request("POST", ELASTIC_SEARCH_POST_URL, data, headers)
            # response = conn.getresponse()
            counter += 1
            if counter % 5000 == 0:
                print "indexing......({count} venues indexed)".format(count=counter)
        print "Done......{count} venues indexed!".format(count=counter)


if __name__ == '__main__':
    main()