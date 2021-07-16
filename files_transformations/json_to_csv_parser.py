import ijson
import pandas as pd
import os
import sys
from shutil import copyfile
from json_file_reader import get_json_keys

def create_empty_dict(dict_keys):
    dict = {}
    for key in dict_keys:
        dict[key] = ""
    return dict

def add_rows_to_csv(rows, csv_file, sorted_columns, include_header):

    #Add rows to a df
    df = pd.DataFrame(rows)

    #Sort the df by json_keys, so that when appending to csv they all respect the same order
    df = df[sorted(sorted_columns)]

    #Append df to csv, add header only in first insertion
    df.to_csv(csv_file, mode='a', index=False, header= include_header)

    print(f'Appended {len(rows)} rows')



def parse_json_to_csv_with_keys(json_filename, json_keys, OUTPUT_FILE):

    df = pd.DataFrame()
    #If output file exists, delete it
    if os.path.exists(OUTPUT_FILE):
        print(f'Removing old version of {OUTPUT_FILE}')
        os.remove(OUTPUT_FILE)

    with open(json_filename, 'rb') as input_file:
        # load json iteratively
        parser = ijson.parse(input_file)

        rows_counter=0

        row = create_empty_dict(json_keys)
        EMPTY_ROW = create_empty_dict(json_keys)

        temp_list_rows = []
        n_rows_to_append_at_a_time = 1000

        for prefix, event, value in parser:
            # print(prefix, event, value)
            # Example
            # prefix: item.KEY
            # event: string
            # value: uuid:59ddb4a4-a431-4386-944a-2ff8db5a1dcf

            #Check if prefix we are reading is a json key, in order to add it to row record
            if len(prefix.split('.'))>1:
                key = prefix.split('.')[1]

                #Add key value to row
                row[key]=value

                if key not in json_keys:
                    # print(f'json_keys detected: {json_keys}')
                    raise Exception (f'WARNING, {key} not in json_keys detected')



            #At the end of each row, save it
            if event == 'end_map':
                #Save row
                temp_list_rows.append(row)
                rows_counter +=1

                #Clean row var
                row = create_empty_dict(json_keys)
                #Every 1000 rows, we will clear the temp_list_rows and append to the csv
                if rows_counter != 0 and rows_counter % n_rows_to_append_at_a_time == 0:

                    add_rows_to_csv(rows = temp_list_rows,
                                    csv_file = OUTPUT_FILE,
                                    sorted_columns = json_keys,
                                    include_header = rows_counter == n_rows_to_append_at_a_time)

                    #Empty temp list of temp_rows
                    temp_list_rows = []

                    print(f'Total rows appended: {rows_counter}')
                    print('%%%%%%%%%%')

        #Once finished, there might still be rows in temp_list_rows that we need to add to the .csv
        if len(temp_list_rows)>0:
            add_rows_to_csv(rows = temp_list_rows,
                            csv_file = OUTPUT_FILE,
                            sorted_columns = json_keys,
                            include_header = rows_counter < n_rows_to_append_at_a_time)

            print(f'Total rows appended: {rows_counter}')
            print('%%%%%%%%%%')
        print(f'OUTPUT_FILE {OUTPUT_FILE}')



def parse_json_to_csv(json_file, csv_file):
    json_keys = get_json_keys(json_file)
    print(f'Got json_keys, its {len(json_keys)} of them!')
    parse_json_to_csv_with_keys(json_file, json_keys, csv_file)

if __name__ == '__main__':
    json_file = sys.argv[1]
    csv_file = sys.argv[2]
    if not os.path.exists(json_file):
        print(f'{json_file} does not exist')
    else:
        parse_json_to_csv(json_file, csv_file)
