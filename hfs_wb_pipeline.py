import argparse

import surveycto_data_downloader

import os
import sys
import time

def parse_args():
    """ Parse command line arguments.
    """
    parser = argparse.ArgumentParser(description="hds_wb_pipeline")

    #Add arguments
    for (argument, arg_help, arg_type, arg_required) in [
           ('--scto_username', 'SurveyCTO username with access to server', str, True),
           ('--scto_password', 'SurveyCTO password', str, True),
           ('--box_folder_id', 'Box folder id', str, True)]:

        parser.add_argument(
            argument,
            help=arg_help,
            default=None,
            required=arg_required,
            type=arg_type
        )

    return parser.parse_args()

if __name__=='__main__':

    args = parse_args()

    server_name = 'hfslatam'
    dir_where_to_save = './data/hfslatam'
    forms_and_json = {
        'hfslatam_560_Chile':'./data/hfslatam/hfslatam-hfslatam_560_Chile-0_1626200279.json',
        'hfslatam_570_Colombia':'Encuesta_BM Colombia.csv',
        'hfslatam_506_cr':'Encuesta_BM_Costa Rica.csv',
        'hfslatam_503_ES':'Encuesta BM_El Salvador.csv',
        'hfslatam_504_Honduras':'Encuesta BM_Honduras.csv',
        'hfslatam_550_Nica':'Encuesta BM_Nicaragua.csv',
        'hfslatam_510_Peru':'Encuesta BM_Peru.csv',
        'hfslatam_809_RepDOm':'Encuesta BM_RepDom.csv',
        'hfslatam_598_Uruguay':'Encuesta BM_ Uruguay.csv'}

    columns_with_attachments = ['audit', 'text_audit']

    box_folder_id = args.box_folder_id

    servername = 'hfslatam'


    username = args.scto_username
    password = args.scto_password

    use_local_copy_json_entries = False

    for form, json_file in forms_and_json.items():

        start = time.time()

        print(f'Working on: {form}')

        print(f'Start timestamp: {start}')

        # #Download survey entries first
        if use_local_copy_json_entries:
            json_full_path = json_file
        else:
            print(f'Downloading entries for {form}')
            json_full_path = surveycto_data_downloader.download_survey_entries(
                        start_day_timespam=0,
                        server_name=servername,
                        form_id=form,
                        username=username,
                        password=password,
                        dir_where_to_save=dir_where_to_save,
                        format='json')

        print(f'json for {form} downloaded. Path: {json_full_path}')

        print(f'Starting attachments download')
        surveycto_data_downloader.download_attachments(
            survey_entries_file = json_full_path,
            attachment_columns = columns_with_attachments,
            dir_box_id= box_folder_id,
            username=username,
            password=password,
            servername=servername,
            formid=form)

        end = time.time()

        print(f'Finished in: {end-start}')
        print()
