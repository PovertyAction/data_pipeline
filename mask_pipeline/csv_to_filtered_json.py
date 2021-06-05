#Reference https://stackoverflow.com/questions/48613557/python-converting-large-csv-file-to-json


import json
import csv
import os
import sys

def filter_row(row_dict):

     selected_keys = ['status_mask', 'status_distance', 'status-agegroup', 'status-gender', 'timestamp', 'uid', 'intro_group-area', 'district_group-ward_village', 'gps-Latitude', 'gps-Longitude', 'gps-Accuracy']

     filtered_row_dict = {key: row_dict[key] for key in selected_keys}

     return filtered_row_dict


def main(csv_file, json_file):

    with open(csv_file, 'r') as input_file:
        reader = csv.DictReader(input_file)


        #Delete if file exists
        if os.path.exists(json_file):
            os.remove(json_file)

        with open(json_file, 'a') as f:

            #Write open bracket
            f.write('[')

            first_row=True
            #Write rows in csv
            for row in reader:

                #We need to write a ',' before writing a new row, only as long as its not the first one
                if first_row:
                    first_row=False
                else:
                    f.write(',\n')

                filtered_row = filter_row(row)
                json.dump(filtered_row, f)


            #Write closing bracket
            f.write(']')


if __name__ == '__main__':

    csv_file = sys.argv[1]
    json_file = sys.argv[2]

    print('Running csv_to_json.py with following parameters')
    print(f'csv_file: {csv_file}')
    print(f'json_file: {json_file}')

    main(csv_file, json_file)
