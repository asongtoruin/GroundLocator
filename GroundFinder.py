from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from time import sleep

import csv

# use Nominatim - Google Maps doesn't seem to work
geolocator = Nominatim()

# open our list of stadia
with open('stadia.csv', 'rb') as stadium_file:
    # read as dictionary - this lets us easily refer to columns
    stadium_csv = csv.DictReader(stadium_file, delimiter=',')

    with open('stadia_located.csv', 'wb') as stadium_output:
        # read the column names from our input, add in Latitude, Longitude and an "Address" category (for checks)
        output_fields = stadium_csv.fieldnames
        output_fields.extend(('Lat', 'Long', 'Address'))

        # again, use the "Dict" versions in CSV for ease of use
        stadium_write = csv.DictWriter(stadium_output, delimiter=',', fieldnames=output_fields)

        # write out field names onto the first row
        stadium_write.writeheader()

        # loop over each team listed
        for row in stadium_csv:

            # this loop waits 10 seconds if the Geocoder times out, and then tries again.
            while True:
                try:
                    # use the "Stadium" and "Location" (i.e. city) fields to form a string to look up
                    find_ground = geolocator.geocode(row['Stadium'] + ',' + row['Location'])
                except GeocoderTimedOut:
                    sleep(10)
                    continue
                break

            # if we haven't got a match, try just looking for the stadium name
            if find_ground is None:
                # again, loop in case of timing out
                while True:
                    try:
                        find_ground = geolocator.geocode(row['Stadium'])
                    except GeocoderTimedOut:
                        sleep(10)
                        continue
                    break

            # if we've got a match, record important details for output
            if find_ground is not None:
                row['Lat'] = find_ground.latitude
                row['Long'] = find_ground.longitude
                row['Address'] = find_ground.address

            # print row

            # write out the updated value
            stadium_write.writerow(row)
