__author__ = 'lli'

import httplib, urllib
import json
import argparse

ELASTIC_SEARCH_HOST = "localhost"
ELASTIC_SEARCH_PORT = "9200"
INDEX_NAME = "test"

ELASTIC_SEARCH_HOST_URL = "{host}:{port}".format(host=ELASTIC_SEARCH_HOST,port=ELASTIC_SEARCH_PORT)


match_all = {
    "query":{
        "match_all":{}
    }
}

def run_delete_post(type,data):
    delete_url = "/{index_name}/{type_name}/_query".format(index_name=INDEX_NAME,type_name=type)
    headers = {"content-type": "application/json"}
    conn = httplib.HTTPConnection(ELASTIC_SEARCH_HOST_URL)
    conn.request("DELETE", delete_url, data, headers)
    response = conn.getresponse()
    print response.status


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--type', required=True, choices=["venue", "stylist", "all"])
    args = parser.parse_args()
    type = args.type
    data = json.dumps(match_all)
    if type == "all":
        run_delete_post("venue", data)
        run_delete_post("stylist", data)
    else:
        run_delete_post(type, data)

if __name__ == '__main__':
    main()