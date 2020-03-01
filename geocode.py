# testing branch, changing functionality to create a whole new table
# Program to geocode addresses from a csv file.

import csv, requests, easygui, os, time, pdb

#apiKey = input('What\'s your Google Maps API key?')
apiKey = 'AIzaSyCmwWaMtacmFN3NZ9UeKHvtaw0TA52yBJM'
mapsUrl = 'https://maps.googleapis.com/maps/api/geocode/json?address='
locationsPath = ''
locations = []
locationsGeo = []

def getCsv():
    global locationsPath
    input('Select a csv with location names in one column. Press Enter when ready.')
    locationsPath = easygui.fileopenbox()
    if '.csv' not in locationsPath:
        input('That\'s not a csv file. Press enter to try again.')
        getCsv()

getCsv()

# pdb.set_trace()

with open(locationsPath, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    locationColumn = easygui.choicebox(msg = 'Which column are locations in?',
                                   title = 'Select column',
                                   choices = reader.fieldnames)
    for row in reader:
        locations.append(row[locationColumn])
    print('Locations are in column "' + locationColumn + '." The first locations listed are:')

    for i in range(0, min(5,len(locations))):
        print(locations[i])
    print('...')

input('Want to continue?')

for location in locations:
    try:
        r = requests.get(mapsUrl + location + '&key=' + apiKey)
        rjson = r.json()
        latlng = rjson['results'][0]['geometry']['location']
        lat = latlng['lat']
        lng = latlng['lng']
        locationsGeo.append([location, lat, lng])
        print('Coordinates added for: ' + location)
    except:
        print('ERROR: Something went wrong geocoding ' + location + '. Press Enter to continue.')
        locationsGeo.append([location, 'Error', 'Error'])

geoCsvPath = os.path.basename(locationsPath)
geoCsvPath = os.path.splitext(geoCsvPath)[0]
geoCsvPath = geoCsvPath + '_geocoded_' + time.strftime("%Y%m%d-%H%M%S") + '.csv'

with open(geoCsvPath, 'w', newline='') as csvfile:
    fieldnames = [locationColumn, 'lat', 'lng']
    writer = csv.DictWriter(csvfile, fieldnames)
    writer.writeheader()
    for i in locationsGeo:
        writer.writerow({locationColumn: i[0], 'lat': i[1], 'lng': i[2]})

input('Geodata saved as: ' + geoCsvPath)
