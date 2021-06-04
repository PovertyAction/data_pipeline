#Reference https://stackoverflow.com/questions/48613557/python-converting-large-csv-file-to-json


import json
import csv
import os
import sys

def main(csv_file):

    with open(csv_file, 'r') as input_file:
        reader = csv.DictReader(input_file)

        jsonoutput = os.path.splitext(csv_file)[0] + '.json'

        #Delete if file exists
        if os.path.exists(jsonoutput):
            os.remove(jsonoutput)

        with open(jsonoutput, 'a') as f:

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

                json.dump(row, f)


            #Write closing bracket
            f.write(']')


if __name__ == '__main__':
    csv_file = sys.argv[1]
    main(csv_file)
