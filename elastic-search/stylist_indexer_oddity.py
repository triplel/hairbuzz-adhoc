__author__ = 'lli'

import argparse
import json
import httplib, urllib
from random import randint
import ast
import names

STYLIST_PSV_SCHEMA = ['hbid', 'first_name', 'last_name', 'gender', 'rating', 'price_rank', 'reviews', 'avatar', 'venue_hbid']

VENUE_PSV_SCHEMA = ['hbid', 'name', 'street_address', 'supplemental_address', 'city', 'neighbourhood', 'state', 'zip',
                    'country', 'phone', 'latitude', 'longitude', 'image']


ODDITY_VENUE_SCHEMA = [(0, 'id'), (1, 'biz_name'), (2, 'biz_info'), (3, 'cat_primary'), (4, 'cat_sub'), (5, 'e_address'),
                       (6, 'e_city'), (7, 'e_state') , (8, 'e_postal'), (9, 'e_zip_full'), (10, 'e_country'), (11, 'loc_county'),
                       (12, 'loc_area_code'), (13, 'loc_FIPS'), (14, 'loc_MSA'), (15, 'loc_PMSA'), (16, 'loc_TZ'), (17, 'loc_DST'),
                        (18, 'loc_LAT_centroid'), (19, 'loc_LAT_poly'), (20, 'loc_LONG_centroid'), (21, 'loc_LONG_poly'), (22, 'biz_phone'),
                        (23, 'biz_phone_ext'), (24, 'biz_fax'), (25, 'biz_email'), (26, 'web_url'), (27, 'web_meta_title'), (28, 'web_meta_desc'),
                        (29, 'web_meta_keys')]


ELASTIC_SEARCH_HOST = "localhost"
ELASTIC_SEARCH_PORT = "9200"
INDEX_NAME = "test"
TYPE_NAME = "stylist"

ELASTIC_SEARCH_HOST_URL = "{host}:{port}".format(host=ELASTIC_SEARCH_HOST,port=ELASTIC_SEARCH_PORT)
ELASTIC_SEARCH_POST_URL = "/{index_name}/{type_name}".format(index_name=INDEX_NAME,type_name=TYPE_NAME)

DEFAULT_VENUE_PICTURE = "https://s3.amazonaws.com/hairbuzz.signup.profile.pics/Studio/salon_inner.jpg"

# e.g.: https://s3.amazonaws.com/hairbvzz/hairstylist/0001.jpg (0001 - 0107)
STYLIST_AVATAR_TEMPLATE = "https://s3.amazonaws.com/hairbvzz/hairstylist/{avatar_id}.jpg"
CURRENT_MAX_ID = 107
GENDER_OPTION_ARRAY = ['f', 'm']


def build_from_oddity_data(data):
    tokens = data.lower().strip("\n").replace('\",\"', '|').replace('\"', '').split("|")
    # hbid = "V00000{id}".format(id=tokens[0])
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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', required=True)
    args = parser.parse_args()
    venues_file = open(args.data)
    # stylists = stylists_file.readlines()

    stylist_count = 13

    for line in venues_file:
        venue_obj = build_from_oddity_data(line)
        stylist_count += 1
        stylist_name_array = names.get_full_name().split(' ')
        first_name = stylist_name_array[0]
        # first_name = "john"
        last_name = stylist_name_array[1]
        # last_name = "doe"
        slug = "{first}{last}{counter}".format(first=first_name[0], last=last_name, counter=stylist_count)
        avatar_url = STYLIST_AVATAR_TEMPLATE.format(avatar_id='{:04}'.format(stylist_count % CURRENT_MAX_ID))
        gender = GENDER_OPTION_ARRAY[randint(0, 1)]
        rating = randint(1, 10)
        price_rank = randint(1, 5)
        reviews = randint(3, 1000)
        stylist_doc = {
            "hbid": "S{:010}".format(stylist_count),
            "first_name": first_name,
            "last_name": last_name,
            "slug": slug,
            "avatar": avatar_url,
            "gender": gender,
            "rating": rating,
            "price_rank": price_rank,
            "reviews": reviews,
            "work_place": venue_obj
        }
        data = json.dumps(stylist_doc)
        print data
        headers = {"content-type": "application/json"}
        conn = httplib.HTTPConnection(ELASTIC_SEARCH_HOST_URL)
        conn.request("POST", ELASTIC_SEARCH_POST_URL, data, headers)
        response = conn.getresponse()
        # print response
        if stylist_count % 5000 == 0:
            print "indexing......({count} stylists indexed)".format(count=stylist_count)
    print "Done......{count} stylists indexed!".format(count=stylist_count)


if __name__ == '__main__':
    main()