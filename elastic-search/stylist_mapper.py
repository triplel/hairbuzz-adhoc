import argparse
import httplib, urllib
import json


ELASTIC_SEARCH_HOST = "localhost"
ELASTIC_SEARCH_PORT = "9200"
INDEX_NAME = "test"
TYPE_NAME = "stylist"

ELASTIC_SEARCH_HOST_URL = "{host}:{port}".format(host=ELASTIC_SEARCH_HOST,port=ELASTIC_SEARCH_PORT)

ELASTIC_SEARCH_MAPPING_URL = "/{index_name}".format(index_name=INDEX_NAME)

ELASTIC_SEARCH_POST_URL = "/{index_name}/{type_name}".format(index_name=INDEX_NAME,type_name=TYPE_NAME)


def mapping_step():
    mapping_json = {
        "mappings": {
            "stylist": {
                "properties": {
                    "hbid": {
                        "type": "string"
                    },
                    "first_name": {
                        "type": "string"
                    },
                    "last_name": {
                        "type": "string"
                    },
                    "slug": {
                        "type": "string"
                    },
                    "avatar": {
                        "type": "string"
                    },
                    "gender": {
                        "type": "string"
                    },
                    "rating": {
                        "type": "long"
                    },
                    "price_rank": {
                        "type": "long"
                    },
                    "reviews": {
                        "type": "long"
                    },
                    "work_place": {
                        "type": "object",
                        "properties": {
                            "hbid": {
                                "type": "string"
                            },
                            "name": {
                                "type": "string"
                            },
                            "address": {
                                "type": "object",
                                "properties": {
                                    "street_address": {
                                        "type": "string"
                                    },
                                    "supplemental_address": {
                                        "type": "string"
                                    },
                                    "city": {
                                        "type": "string"
                                    },
                                    "neighbourhood": {
                                        "type": "string"
                                    },
                                    "state": {
                                        "type": "string"
                                    },
                                    "zip": {
                                        "type": "string"
                                    },
                                    "country": {
                                        "type": "string"
                                    }
                                }
                            },
                            "coordinates": {
                                "type": "geo_point"
                            },
                            "phone": {
                                "type": "string"
                            },
                            "image": {
                                "type": "string"
                            }
                        }

                    }
                }
            }
        }
    }
    data = json.dumps(mapping_json)
    headers = {"content-type": "application/json"}
    http_connection = httplib.HTTPConnection(ELASTIC_SEARCH_HOST_URL)
    http_connection.request("PUT", ELASTIC_SEARCH_MAPPING_URL, data, headers)
    response = http_connection.getresponse()
    print "Mapping Stylist Done -> (Response:{res})".format(res=response.status)


def main():
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
    mapping_step()

if __name__ == '__main__':
    main()