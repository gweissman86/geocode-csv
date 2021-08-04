# Program to geocode addresses from a csv file.

import configparser, csv, requests, os, time, pdb

config = configparser.ConfigParser()
config.read('config.ini')

mapsUrl = 'https://maps.googleapis.com/maps/api/geocode/json?address='
location_path = config['settings']['csv_path']
location_column = config['settings']['location_column']
api_key = os.environ['APIKEY'] if 'APIKEY' in os.environ else config['settings']['api_key']
locations = []
locationsGeo = []
new_csv_list = []
result_directory = os.path.dirname(location_path)

input('This program will lookup latitude and longitude information contained in a single column of a csv file. Before you start, fill out config.ini with Google maps API, csv file path, and location column.') 

if not api_key:
    input('You need to enter an API key')
    quit()

if 'csv' not in location_path:
    input('You have not selected a csv file. Fix config.ini and try again.')
    quit()


with open(location_path, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    if location_column not in reader.fieldnames:
        input('location_column not found in selected CSV. Try again.')
        quit()
    print(location_column + '." The first locations listed are:')
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
            r = requests.get(mapsUrl + location + '&key=' + api_key)
            rjson = r.json()
            latlng = rjson['results'][0]['geometry']['location']
            lat = latlng['lat']
            lng = latlng['lng']
            new_row['lat'] = lat
            new_row['lng'] = lng
            new_csv_list.append(new_row)
            print('Coordinates added for: ' + location)
        except:
            new_row['lat'] = 'ERROR'
            new_row['lng'] = 'ERROR'
            new_csv_list.append(new_row)
            print('ERROR: Something went wrong geocoding ' + location + '. Press Enter to continue.')

if not os.path.exists(result_directory):
    os.mkdir(result_directory)

geoCsvPath = os.path.basename(location_path)
geoCsvPath = os.path.splitext(geoCsvPath)[0]
geoCsvPath = geoCsvPath + '_geocoded_' + time.strftime("%Y%m%d-%H%M%S") + '.csv'
geoCsvPath = os.path.join(result_directory, geoCsvPath)


with open(geoCsvPath, 'w', newline='') as csvfile:
    fieldnames = list(new_csv_list[0].keys())
    writer = csv.DictWriter(csvfile, fieldnames)
    writer.writeheader()
    for i in new_csv_list:
        writer.writerow(i)

input('Geodata saved as: ' + geoCsvPath)
