#!/usr/bin/env bash
#todo - create collections
#todo - set unique indexes
python database/mongodb/rebuild_venue_collection.py --venue resources/test_data/venues.psv
python database/mongodb/rebuild_stylist_collection.py --stylist resources/test_data/stylists.psv --venue resources/test_data/venues.psv
python database/mongodb/rebuild_customer_collection.py --customer resources/test_data/customers.psv
echo "MongoDB dev database rebuild completed!"
