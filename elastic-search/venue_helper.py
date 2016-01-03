import json


DEFAULT_VENUE_PICTURE = "https://s3.amazonaws.com/hairbuzz.signup.profile.pics/Studio/salon_inner.jpg"


def build_from_oddity_data(data):
    tokens = data.lower().strip("\n").replace('\"', '').split(",")
    hbid = "V00000{id}".format(id=tokens[0])
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
