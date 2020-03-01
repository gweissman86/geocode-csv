# testing branch, changing functionality to create a whole new table
# Program to geocode addresses from a csv file.

import csv, requests, easygui, os, time, pdb

#apiKey = input('What\'s your Google Maps API key?')
apiKey = 'AIzaSyCmwWaMtacmFN3NZ9UeKHvtaw0TA52yBJM'
mapsUrl = 'https://maps.googleapis.com/maps/api/geocode/json?address='
location_path = ''
location_column = ''
locations = []
locationsGeo = []
new_csv_list = []

def getCsv():
    global location_path
    input('Select a csv with location names in one column. Press Enter when ready.')
    location_path = easygui.fileopenbox()
    if '.csv' not in location_path:
        input('That\'s not a csv file. Press enter to try again.')
        getCsv()

getCsv()

with open(location_path, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    location_column = easygui.choicebox(msg = 'Which column are locations in?',
                                   title = 'Select column',
                                   choices = reader.fieldnames)
    print('Locations are in column "' +
          location_column + '." The first locations listed are:')
    for i in range(0, 5):
        try:
            place = reader.__next__()
            print(place[location_column])
        except:
            break

input('Want to continue?')

with open(location_path, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        location = row[location_column]
        new_row = row
        try:
            r = requests.get(mapsUrl + location + '&key=' + apiKey)
            rjson = r.json()
            latlng = rjson['results'][0]['geometry']['location']
            lat = latlng['lat']
            lng = latlng['lng']
            new_row['lat'] = lat
            new_row['lng'] = lng
            new_csv_list.append(new_row)
            print('Coordinates added for: ' + location)
        except:
            print('ERROR: Something went wrong geocoding ' + location + '. Press Enter to continue.')
            locationsGeo.append([location, 'Error', 'Error'])

geoCsvPath = os.path.basename(location_path)
geoCsvPath = os.path.splitext(geoCsvPath)[0]
geoCsvPath = geoCsvPath + '_geocoded_' + time.strftime("%Y%m%d-%H%M%S") + '.csv'

with open(geoCsvPath, 'w', newline='') as csvfile:
    fieldnames = list(new_csv_list[0].keys())
    writer = csv.DictWriter(csvfile, fieldnames)
    writer.writeheader()
    for i in new_csv_list:
        writer.writerow(i)

input('Geodata saved as: ' + geoCsvPath)
