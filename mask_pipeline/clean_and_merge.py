# import ijson
import pandas as pd
import os
import sys
import json
import numpy as np
# from shutil import copyfile
# from json_file_reader import get_json_keys
from csv import reader, writer
import time

BANGLADESH = 'Bangladesh'

def validate_inputs(file_a, file_b):
    #Check that files exist
    for file in [file_a, file_b]:
        if not os.path.exists(file):
            print(f'{file} does not exist')
            return False

    return True


def get_country(parent_file_name):
    #PENDING
    return BANGLADESH

def clean_parent_df(df, parent_file_name):

    #Cleaning for bangladesh
    if get_country(parent_file_name) == BANGLADESH:

        #Value label replacements
        intro_group_area_replacements_dict = \
            {1:"Gabtali bus terminal", 2:"Mohammadpur town hall", 3:"Mohammadpur bus stand",
            4:"Mohammadpur Shia Mosque", 5:"Farmgate area", 6:"Badda and notun market areas",
            7:"Mirpur-1 Golchottor, Shah Ali Market", 8:"Mirpur-10 Golchottor",
            9:"Bashundhara City Shopping Mall", 10:"Jamuna Future Park Shopping Mall",
            11:"Uttara Muscat Plaza Shopping Mall", 12:"Uttara Rajalakshi Shopping Mall",
            13:"Mohakhali bus terminal"}

        #Add extra columns
        upazila_replacement_dict = \
                {"Gabtali bus terminal":"Darus Salam", "Mohammadpur town hall":"Mohammadpur", "Mohammadpur bus stand":"Mohammadpur",
                "Mohammadpur Shia Mosque":"Mohammadpur", "Farmgate area":"Tejgaon", "Badda and notun market areas":"Badda",
                "Mirpur-1 Golchottor, Shah Ali Market":"Mirpur", "Mirpur-10 Golchottor":"Mirpur",
                "Bashundhara City Shopping Mall":"Sher-E-Bangla Nagar", "Jamuna Future Park Shopping Mall":"Khilkhet",
                "Uttara Muscat Plaza Shopping Mall":"Uttara", "Uttara Rajalakshi Shopping Mall":"Uttara",
                "Mohakhali bus terminal":"Tejgaon"}


        union_replacement_dict = \
                {"Gabtali bus terminal":"Ward No-10", "Mohammadpur town hall":"Ward No-31", "Mohammadpur bus stand":"Ward No-33",
                "Mohammadpur Shia Mosque":"Ward No-33", "Farmgate area":"Ward No-27", "Badda and notun market areas":"Ward No-21",
                "Mirpur-1 Golchottor, Shah Ali Market":"Ward No-8", "Mirpur-10 Golchottor":"Ward No-3",
                "Bashundhara City Shopping Mall":"Ward No-27", "Jamuna Future Park Shopping Mall":"Ward No-17",
                "Uttara Muscat Plaza Shopping Mall":"Ward No-1", "Uttara Rajalakshi Shopping Mall":"Ward No-1",
                "Mohakhali bus terminal":"Ward No-20"}
                

        district_replacement_dict = \
                {"Gabtali bus terminal":"Dhaka", "Mohammadpur town hall":"Dhaka", "Mohammadpur bus stand":"Dhaka",
                "Mohammadpur Shia Mosque":"Dhaka", "Farmgate area":"Dhaka", "Badda and notun market areas":"Dhaka",
                "Mirpur-1 Golchottor, Shah Ali Market":"Dhaka", "Mirpur-10 Golchottor":"Dhaka",
                "Bashundhara City Shopping Mall":"Dhaka", "Jamuna Future Park Shopping Mall":"Dhaka",
                "Uttara Muscat Plaza Shopping Mall":"Dhaka", "Uttara Rajalakshi Shopping Mall":"Dhaka",
                "Mohakhali bus terminal":"Dhaka"}


        division_replacement_dict = \
                {"Gabtali bus terminal":"Dhaka", "Mohammadpur town hall":"Dhaka", "Mohammadpur bus stand":"Dhaka",
                "Mohammadpur Shia Mosque":"Dhaka", "Farmgate area":"Dhaka", "Badda and notun market areas":"Dhaka",
                "Mirpur-1 Golchottor, Shah Ali Market":"Dhaka", "Mirpur-10 Golchottor":"Dhaka",
                "Bashundhara City Shopping Mall":"Dhaka", "Jamuna Future Park Shopping Mall":"Dhaka",
                "Uttara Muscat Plaza Shopping Mall":"Dhaka", "Uttara Rajalakshi Shopping Mall":"Dhaka",
                "Mohakhali bus terminal":"Dhaka"}

        
        df['intro_group-area']      = df['intro_group-area'].replace(intro_group_area_replacements_dict)
        df['intro_group-division']  = df['intro_group-area'].replace(division_replacement_dict)
        df['intro_group-district']  = df['intro_group-area'].replace(district_replacement_dict)
        df['intro_group-upazila']   = df['intro_group-area'].replace(upazila_replacement_dict)
        df['intro_group-union']     = df['intro_group-area'].replace(union_replacement_dict)

        #Change instance_date = "2021-05-08" to "2021-05-09"
        df['instance_date'] = df['instance_date'].replace(['2021-05-08'],'2021-05-09')

        #Adding treatment and baseline indicators
        #@Mehrab confirm column names and values
        df['baseline'] = np.where(df['instance_date']== '2021-05-09', 'Baseline', 'Rest')

        #Change instance_date to data type
        df['instance_date'] = pd.to_datetime(df['instance_date'])

        #Drop if key == "uuid:20037a8b-8bd5-493f-b77b-3c00042c1d96"
        df = df[df['KEY'] != "uuid:20037a8b-8bd5-493f-b77b-3c00042c1d96"]

        return df


def replace_values_with_labels(row_dict, parent_file_name):

    columns_and_value_labels_for_replacement = \
        {'status-mask': {'0':'No mask', '1':'Non-mask face covering', '6':'Any Mask - PROPERLY', '7':'Any Mask - IMPROPERLY'},
        'status-distance': {'1':"Someone within arm's length", '0':"Someone within arm's length"},
        'status-gender': {'1':"Male", '2':"Female"},
        'status-agegroup': {'1':"Young (below 30)", '2':"Middle-age (30-50)", '3':"Old (50+)"}
        }




    if get_country(parent_file_name) == BANGLADESH:

        for column, value_label_dict in columns_and_value_labels_for_replacement.items():

            #Replace in row_dict the value in every column by its label according to value_label_dict

            if row_dict[column] in value_label_dict: #We expect this always to be true if columns_and_value_labels_for_replacement is complete
                row_dict[column] = value_label_dict[row_dict[column]]

    return row_dict

def add_rows_to_csv(rows, csv_file, sorted_columns, include_header):

    #Add rows to a df
    df = pd.DataFrame(rows)

    #Sort the df by json_keys, so that when appending to csv they all respect the same order
    df = df[sorted(sorted_columns)]

    #Append df to csv
    df.to_csv(csv_file, mode='a', index=False, header= include_header)

    print(f'Appended {len(rows)} rows')

def clean_and_merge_files(parent_file_name, repeatgroup_file_name, merged_file_path):
    '''
    This method will merge repeatgroup_file_name with parent_file_name, creating a new file
    We expect parent_file_name to be small, and hence for us to be able to load it fully to memory
    On the other hand, we expect repeatgroup_file_name to be big, so we will process it one line at a time
    '''

    start_time = time.time()

    #Delete output file if exists
    if os.path.exists(merged_file_path):
        os.remove(merged_file_path)

    parent_df = pd.read_csv(parent_file_name)

    parent_df = clean_parent_df(parent_df, parent_file_name)

    #Select parent columns we want to add to each repeatgroup row
    #@Mehrab include more if we want
    parent_cols_to_discard = ['KEY', 'SET-OF-ind_group']
    parent_cols_to_add = [c for c in parent_df.columns if c not in parent_cols_to_discard]

    # Traverse repeatgroup_file_name line by line, merging with parent_file_name
    # skip first line i.e. read header first and then iterate over each row of the csv as a list
    with open(repeatgroup_file_name, 'r') as read_obj:
        csv_reader = reader(read_obj)
        repeatgroup_file_columns = next(csv_reader)

        # Check file is not empty
        if repeatgroup_file_columns == None:
            raise ValueError(f'{repeatgroup_file_columns} is empty')

        #Define columns in output file
        merged_file_columns = repeatgroup_file_columns + parent_cols_to_add

        rows_to_append_to_file = []
        rows_counter = 0
        #Loop over every row in repeatgroup_file_name
        for row in csv_reader:

            #Row dict we will be used for merging
            new_row = {}

            #Iterate over row elements, adding it to new_row dict with its respective key
            for index, row_element in enumerate(row):
                new_row[repeatgroup_file_columns[index]] = str(row_element)

            new_row = replace_values_with_labels(new_row, parent_file_name)

            #Merge new_row with info from parent_df

            #Get parent row associated to this row
            parent_row = parent_df[parent_df['KEY'] == new_row['PARENT_KEY']]

            #If no parent_row was found (case we have dropped their key), do not consider this observations and move to next row
            if parent_row.shape[0]==0:
                continue

            #Add selected columns of parent_row to new_role
            for col in parent_cols_to_add:
                #Add info to dict
                new_row[col] = str(parent_row[col].iloc[0])


            #Save row in list of rows ready to be appended to file
            rows_to_append_to_file.append(new_row)
            rows_counter +=1

            #Every x rows, we will append rows to csv and clear rows_to_append_to_file
            n_rows_to_append_per_iteration = 10000

            if rows_counter != 0 and rows_counter % n_rows_to_append_per_iteration == 0:



                add_rows_to_csv(rows = rows_to_append_to_file,
                                csv_file = merged_file_path,
                                sorted_columns = merged_file_columns,
                                include_header = rows_counter == n_rows_to_append_per_iteration)

                print(f'Total rows appended: {rows_counter}')
                print('%%%%%%%%%%')

                #Clear list of rows to append
                rows_to_append_to_file = []


        #Once finished looping over all rows, there might still be rows in rows_to_append_to_file that we need to add to the .csv
        if len(rows_to_append_to_file)>0:
            add_rows_to_csv(rows = rows_to_append_to_file,
                            csv_file = merged_file_path,
                            sorted_columns = merged_file_columns,
                            include_header = rows_counter < n_rows_to_append_per_iteration)

            print(f'Total rows appended: {rows_counter}')



        end_time = time.time()
        print(f'Finished in: {end_time - start_time}')
        print(f'n_rows_to_append_per_iteration: {n_rows_to_append_per_iteration}')


def main(parent_file_name, repeatgroup_file_name, output_file):

    valid_inputs = validate_inputs(parent_file_name, repeatgroup_file_name)
    if not valid_inputs:
        sys.exit(1)

    clean_and_merge_files(parent_file_name, repeatgroup_file_name, output_file)


if __name__ == '__main__':
    parent_file_name = sys.argv[1]
    repeatgroup_file_name = sys.argv[2]
    output_file = sys.argv[3]

    print('Running cleand_and_merge.py with following parameters')
    print(f'parent_file_name: {parent_file_name}')
    print(f'repeatgroup_file_name: {repeatgroup_file_name}')
    print(f'output_file: {output_file}')


    main(parent_file_name, repeatgroup_file_name, output_file)


# Total rows appended: 173605
# Finished in: 766.136253118515
# n_rows_to_append_per_iteration: 5000
