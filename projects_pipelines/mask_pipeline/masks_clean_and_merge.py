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

from cleaning_values import cleaning_values

def validate_inputs(file_a, file_b):
    #Check that files exist
    for file in [file_a, file_b]:
        if not os.path.exists(file):
            raise Exception(f'{file} does not exist')


def replace_values_in_column(df, destiny_column, origin_column, replacements_dict):

    print(df.columns)

    df[destiny_column] = \
        df[origin_column].replace(replacements_dict)

    return df

def replace_values(df, server_formid):
    #Value label replacements

    #Get replacements for this parent_file_name
    replacements = cleaning_values.replacements[server_formid]

    if server_formid == 'bdmaskrct_mask_monitoring_form_bn':

        for (destiny_column, origin_column, replacements_dict) in \
            [('intro_group-area', 'intro_group-area', replacements['intro_group_area_replacements_dict']),
            ('intro_group-division', 'intro_group-area', replacements['division_replacement_dict']),
            ('intro_group-district', 'intro_group-area', replacements['district_replacement_dict']),
            ('intro_group-upazila', 'intro_group-area', replacements['upazila_replacement_dict']),
            ('intro_group-union', 'intro_group-area', replacements['union_replacement_dict'])]:

            df = replace_values_in_column(df, destiny_column, origin_column, replacements_dict)

    return df


def drop_values(df, server_formid):

    keys_to_drop = cleaning_values.keys_to_drop[server_formid]

    for key_to_drop in keys_to_drop:
        df = df[df['KEY'] != key_to_drop]

    return df

def form_specifics_cleaning (df, server_formid):

    if server_formid == 'bdmaskrct_mask_monitoring_form_bn':
        #Change instance_date = "2021-05-08" to "2021-05-09"
        df['instance_date'] = df['instance_date'].replace(['2021-05-08'],'2021-05-09')

    return df

def clean_parent_df(df, server_formid):

    df = replace_values(df, server_formid)

    df = form_specifics_cleaning (df, server_formid)

    #Adding treatment and baseline indicators
    df['baseline'] = np.where(df['instance_date']== '2021-05-09', 'Baseline', 'Rest')

    #Change instance_date to data type
    df['instance_date'] = pd.to_datetime(df['instance_date'])

    #Drop specific keys
    df = drop_values(df, server_formid)

    return df


def replace_values_with_labels(row_dict, server_formid):

    columns_and_value_labels_for_replacement = cleaning_values.columns_and_value_labels_for_replacement[server_formid]

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

def clean_and_merge_files(parent_file_name, repeatgroup_file_name, merged_file_path, server_formid):
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

    parent_df = clean_parent_df(parent_df, server_formid)

    #Select parent columns we want to add to each repeatgroup row
    parent_cols_to_discard = cleaning_values.parent_cols_to_discard[server_formid]
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

            new_row = replace_values_with_labels(new_row, server_formid)

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


def main(parent_file_name, repeatgroup_file_name, output_file, server_formid):

    validate_inputs(parent_file_name, repeatgroup_file_name)

    clean_and_merge_files(parent_file_name, repeatgroup_file_name, output_file, server_formid)


if __name__ == '__main__':
    arg_parent_file_name = sys.argv[1]
    arg_repeatgroup_file_name = sys.argv[2]
    arg_output_file = sys.argv[3]
    arg_server_formid = sys.argv[4]

    print('Running masks_clean_and_merge.py with following parameters')
    print(f'parent_file_name: {arg_parent_file_name}')
    print(f'repeatgroup_file_name: {arg_repeatgroup_file_name}')
    print(f'output_file: {arg_output_file}')
    print(f'server_formid: {arg_server_formid}')


    main(arg_parent_file_name, arg_repeatgroup_file_name, arg_output_file, arg_server_formid)
