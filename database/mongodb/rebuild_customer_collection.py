__author__ = 'lli'

import argparse
import json
import pymongo
from pymongo import MongoClient
import ast

#
# def recreate_stylist_collection(collection):
#

# C0000000001|jleto1|JLeto|Jared|Leto|device_id_159223123|m|http://img.allw.mn/content/movies/2013/08/18_jared-leto.jpg|2127362512|jared.leto@me.com|jared.leto|||||jared.leto|true
# C0000000002|bdylan1|dylan_musician|Bob|Dylan|device_id_159212131223|m|http://soniceditions.com/library/bob-dylan-5WFW_o_tn.jpg|2127822514|bob@dylanrecords.com|bob.dylan|||||bob.dylan|true
# C0000000003|cevans1|Captain America|Chris|Evans|device_id_12312124912|m|https://pbs.twimg.com/profile_images/605082381528096769/gt_sJRot_400x400.png||chris@newargehair.com|chris.evans|||||chris.evans|true

CUSTOMER_SCHEMA = ["hbid", "slug", "display_name", "first_name", "last_name", "device_id", "gender", "avatar", "phone", "email",
                   "facebook_name", "twitter_name", "instagram_name", "google_name", "registered"]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--customer', required=True)
    args = parser.parse_args()
    customer_file = open(args.customer)
    customer_list = []
    for line in customer_file:
        tokens = line.lower().strip("\r").strip("\n").split("|")
        customer_doc = {
            "hbid": tokens[0],
            "slug": tokens[1],
            "display_name": tokens[2],
            "first_name": tokens[3],
            "last_name": tokens[4],
            "device_id": tokens[5],
            "gender": tokens[6],
            "avatar": tokens[7],
            "phone": tokens[8],
            "email": tokens[9],
            "social_networks": {
                "facebook_username": tokens[10],
                "twitter_username": tokens[11],
                "instagram_username": tokens[12],
                "tumblr_username": tokens[13],
                "google_username": tokens[14]
            },
            "registered": bool(tokens[15])
        }
        # print customer_doc
        customer_list.append(customer_doc)

    client = MongoClient('localhost', 27017)
    hb_dev = client.dev
    # print cip_test.collection_names()
    customer_collection = hb_dev.customers
    # clean up the collection before reinserting
    customer_collection.drop()

    # customer_collection.ensure_index([("hbid", 1), ("slug", 1), ("email", 1),
    #                                   ("social.facebook_username", 1), ("social_networks.twitter_username", 1),
    #                                   ("social_networks.instagram_username", 1), ("social_networks.tumblr_username", 1),
    #                                   ("social_networks.google_username", 1)], unique=True)


    customer_collection.ensure_index([("hbid", 1), ("slug", 1), ("email", 1)], unique=True)



    customer_collection.insert(customer_list)

    print "{count} customers inserted in customers collection".format(count=customer_collection.count())


if __name__ == '__main__':
    main()
