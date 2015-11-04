#!/usr/bin/env bash
python database/mongodb/rebuild_venue_collection.py --venue resources/test_data/venues.psv
python database/mongodb/rebuild_stylist_collection.py --stylist resources/test_data/stylists.psv --venue resources/test_data/venues.psv
echo "MongoDB dev database rebuild completed!"
