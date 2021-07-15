'''
This script transforms a csv file to json format, keeping only a selection of columns(keys)
Reference https://stackoverflow.com/questions/48613557/python-converting-large-csv-file-to-json
'''

import json
import csv
import os
import sys

def filter_row(row_dict, selected_keys):

     filtered_row_dict = {key: row_dict[key] for key in selected_keys}
     return filtered_row_dict

def main(csv_file, json_file, selected_keys):

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

                filtered_row = filter_row(row, selected_keys)
                json.dump(filtered_row, f)


            #Write closing bracket
            f.write(']')


if __name__ == '__main__':

    arg_csv_file = sys.argv[1]
    arg_json_file = sys.argv[2]

    arg_selected_keys = sys.argv[3].split(',')



    print('Running csv_to_json.py with following parameters')
    print(f'csv_file: {arg_csv_file}')
    print(f'json_file: {arg_json_file}')
    print(f'selected_keys: {arg_selected_keys}')

    main(arg_csv_file, arg_json_file, arg_selected_keys)
