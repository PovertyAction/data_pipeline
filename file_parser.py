import ijson
import pandas as pd
import os
import sys


def create_empty_dict(dict_keys):
    dict = {}
    for key in dict_keys:
        dict[key] = ""
    return dict

def get_all_keys(json_filename):

    all_keys = []

    with open(json_filename, 'rb') as input_file:
        # load json iteratively
        parser = ijson.parse(input_file)
        for prefix, event, value in parser:
            #Check if prefix we are reading is a json key
            if len(prefix.split('.'))>1:
                key = prefix.split('.')[1]

                if key not in all_keys:
                    all_keys.append(key)
    return all_keys


def add_rows_to_csv(rows, csv_file, sorted_columns, include_header):

    #Add rows to a df
    df = pd.DataFrame(rows)

    #Sort the df by json_keys, so that when appending to csv they all respect the same order
    df = df[sorted(sorted_columns)]

    #Append df to csv, add header only in first insertion
    df.to_csv(csv_file, mode='a', index=False, header= include_header)

    print(f'Appended {len(rows)} rows')



def parse_json_to_csv_with_keys(json_filename, json_keys):

    df = pd.DataFrame()
    #If output file exists, delete it
    OUTPUT_FILE = os.path.basename(json_filename).split('.')[0]+'.csv'
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

        for prefix, event, value in parser:
            #Check if prefix we are reading is a json key
            if len(prefix.split('.'))>1:
                key = prefix.split('.')[1]

                #First lets check we are not starting a new row. If we are, we should save the previous one and start a new one
                if key == 'CompletionDate' and row != EMPTY_ROW:
                    temp_list_rows.append(row)
                    rows_counter +=1
                    row = create_empty_dict(json_keys)

                    n_rows_to_append_at_a_time = 1000
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


                #Add key value to row
                row[key]=value

        #Once finished, there might still be rows in temp_list_rows that we need to add to the .csv
        if len(temp_list_rows)>0:
            add_rows_to_csv(rows = temp_list_rows,
                            csv_file = OUTPUT_FILE,
                            sorted_columns = json_keys,
                            include_header = False)

            print(f'Total rows appended: {rows_counter}')
            print('%%%%%%%%%%')
        print(f'OUTPUT_FILE {OUTPUT_FILE}')

def parse_json_to_csv(json_file):
    json_keys = get_all_keys(json_file)
    print(f'Got json_keys, its {len(json_keys)} of them!')
    parse_json_to_csv_with_keys(json_file, json_keys)

if __name__ == '__main__':
    json_file = sys.argv[1]
    parse_json_to_csv(json_file)
