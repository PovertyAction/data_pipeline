import ijson
import pandas as pd
import os
import sys
import requests
import ntpath
import time
import csv

sys.path.append(os.path.join(os.path.dirname(__file__),'../box'))
import box_manager

def get_local_list_files(dir_path):

    if os.path.isdir(dir_path):
        list_files = []
        print(f'Getting list of files in {dir_path}')
        for dirpath, dirnames, filenames in os.walk(dir_path):

            if dirpath == dir_path:
                list_files = filenames

        print(f'Finished getting list of files. Its {len(list_files)} of them')
        return list_files
    else:
        print(f'{dir_path} is not a directory')
        return False

def get_list_files(dir_path = None, dir_box_id = None):
    '''
    Gets list of files either in a giver directory path or in a box folder in the cloud
    '''
    print(f'Running get_list_files for {dir_box_id}')
    if dir_path and dir_box_id:
        print(f'Must provide dir_path OR dir_box_id')
        return False

    if dir_path:
        return get_local_list_files(dir_path)

    elif dir_box_id:
        return box_manager.get_list_files('jwt', dir_box_id)


def safe_delete(file_path):
    try:
        os.remove(file_path)
    except Excepion as e:
        print("An exception occurred in safe_delete")
        raise Exception(e)

def run_surveycto_api_download_request(file_url, username, password, encryption_key):

    try:
        headers = {'X-OpenRosa-Version': '1.0'}
        auth_basic = requests.auth.HTTPBasicAuth(
            username=username,
            password=password)

        if encryption_key:
            files = {'private_key': open(encryption_key, 'rb')}
            response = requests.post(file_url,
                                    files=files,
                                    headers = headers,
                                    auth = auth_basic)
        else:
            response = requests.get(file_url,
                                 headers = headers,
                                 auth = auth_basic)

        return response

    except Exception as e:
        print("An exception occurred")
        print(e)
        return False

def download_file_from_surveycto(file_url,
                                username,
                                password,
                                file_name,
                                dir_path_where_to_save=None,
                                box_folder_id=None,
                                encryption_key=False):
    '''
    Uses surveycto api to download file to local or to box
    '''
    print(f'Starting download of {file_url}')

    if dir_path_where_to_save:
        #Create dir_path_where_to_save if it does not exist
        if not os.path.exists(dir_path_where_to_save):
            os.makedirs(dir_path_where_to_save)

        file_path = os.path.join(dir_path_where_to_save, file_name)

    #If files should be downloaded to box directly, we will download a local copy first, push to box and then delete
    elif box_folder_id:
        tmp_folder = os.path.join('data','tmp')
        #Create tmp folder if it does not exist
        if not os.path.exists(tmp_folder):
            os.makedirs(tmp_folder)
        file_path = os.path.join(tmp_folder, file_name)

    else:
        raise ValueError('dir_path_where_to_save and box_folder_id are None')

    response = run_surveycto_api_download_request(file_url, username, password, encryption_key)

    #Check if error status code
    if response.status_code != 200:
        error_msg = f'Error {response.status_code} when downloading {file_url}. '
        error_msg += response.text
        raise Exception(error_msg)

    #Save response content in file
    data = response.content

    f = open(file_path, 'wb')
    f.write(data)
    f.close()

    #If file was supposed to be saved locally,return
    if dir_path_where_to_save:
        return

    #If file was supposed to be saved in box directly, push to box and delete local copy
    if box_folder_id:

       #Upload file to box
       box_manager.upload_file('jwt', box_folder_id, file_path)

       #Delete file from local
       safe_delete(file_path)




def download_survey_entries(start_day_timespam, server_name, form_id, username, password, dir_where_to_save, format='json'):

    now_timespam = int(time.time())

    if format =='json':
        file_url = f'https://{server_name}.surveycto.com/api/v2/forms/data/wide/json/{form_id}?date={start_day_timespam}'
        file_name = f'{server_name}-{form_id}-{start_day_timespam}_{now_timespam}.json'
    elif format == 'csv':
        file_url = f'https://{server_name}.surveycto.com/api/v1/forms/data/wide/csv/{form_id}?date={start_day_timespam}'
        file_name = f'{server_name}-{form_id}-{start_day_timespam}_{now_timespam}.csv'
    else:
        raise ValueError(f'{format} not valid format')

    download_file_from_surveycto(file_url=file_url,
                                username=username,
                                password=password,
                                file_name=file_name,
                                dir_path_where_to_save=dir_where_to_save)

    return os.path.join(dir_where_to_save,file_name)

def get_file_extension(file_path):
    split_tup = os.path.splitext(file_path)
    file_extension = split_tup[1]
    return file_extension

def file_already_downloaded(file_name, dir_path=None, dir_box_id=None):

    if dir_path:
        return os.path.isfile(file_name)

    elif dir_box_id:
        try:
            file_exists = box_manager.check_file_exists_in_folder('jwt', dir_box_id, file_name)
            return file_exists
        except Exception as e:
            raise Exception(str(e))


def check_if_file_exists_or_download_it(file_name,
                                        file_url,
                                        username,
                                        password,
                                        dir_path=None,
                                        dir_box_id=None,
                                        encryption_key=None):

    #Check if file has already been downloaded. If it does, return.

    if file_already_downloaded(file_name, dir_path, dir_box_id):
        print(f'{file_name} already downloaded')
        print('')
        return True

    #Else, proceed to download

    #Download file to local Or download to box directly (download local, push box, delete local)
    download_file_from_surveycto(
            file_url=file_url,
            username=username,
            password=password,
            file_name=file_name,
            dir_path_where_to_save=dir_path,
            box_folder_id=dir_box_id,
            encryption_key=encryption_key)

    # sys.exit(1)

def download_attachments_from_json(
                        attachment_columns,
                        username,
                        password,
                        survey_entries_file,
                        servername=None,
                        formid=None,
                        dir_path=None,
                        dir_box_id=None,
                        encryption_key=None):

    with open(survey_entries_file, 'rb') as input_file:
        # load json iteratively
        parser = ijson.parse(input_file)
        for prefix, event, value in parser:
            #Check if prefix we are reading is a json key
            #We know json keys come in the shape "prefix.key"
            if len(prefix.split('.'))>1:
                key = prefix.split('.')[1]

                #Print submission date for refference
                if key == 'SubmissionDate':
                   print(value)

                #Check if key is associated to one of columns with urls to download, and that value associated to key is not null
                if key in attachment_columns and value !='':

                    #Get file_name
                    file_name = ntpath.basename(value)

                    #value has the full url to files to download
                    print(file_name)
                    check_if_file_exists_or_download_it(file_name=file_name,
                                                        file_url=value,
                                                        username=username,
                                                        password=password,
                                                        dir_path=dir_path,
                                                        dir_box_id=dir_box_id)

def download_attachments_from_csv(attachment_columns,
                        username,
                        password,
                        survey_entries_file,
                        servername,
                        formid,
                        dir_path=None,
                        dir_box_id=None, encryption_key=None):


    with open(survey_entries_file, 'r') as read_obj:
        csv_reader = csv.reader(read_obj)
        header = next(csv_reader)

        # Check file as empty
        if header != None:
            # Iterate over each row after the header in the csv
            # row variable is a list that represents a row in csv
            for row in csv_reader:
                #download all atachments for this row
                for c in attachment_columns:

                    #Get c index in list
                    c_index = header.index(c)

                    #Get file_name (extract /media/ from path)
                    file_name = ntpath.basename(row[c_index])

                    #Check if file_name is empty, skip if thats the case
                    if file_name is None or file_name =='':
                        print(f'file_name is empty for {c}')
                        continue

                    #Build file_url
                    uuid = row[header.index('KEY')]

                    if servername is None or formid is None:
                        raise ValueError('servername or formid is None')

                    file_url = f'https://{servername}.surveycto.com/api/v2/forms/{formid}/submissions/{uuid}/attachments/{file_name}'

                    check_if_file_exists_or_download_it(file_name=file_name,
                                                        file_url=file_url,
                                                        username=username,
                                                        password=password,
                                                        dir_path=dir_path,
                                                        dir_box_id=dir_box_id)

def validate_destination(dir_path, dir_box_id):
    #Validate that either dir_path or dir_box_id
    return True

def download_attachments(survey_entries_file,
                        attachment_columns,
                        username,
                        password,
                        servername=None,
                        formid=None,
                        dir_path=None,
                        dir_box_id=None,
                        encryption_key=None):
    '''
    Download attachments for given survey entries.
    Inputs:
    - survey_entries_file: file with survey entries, which will contain columns with attachments urls
    - attachment_columns: columns in main survey_entries_file for which downloads must be triggered
    - username and password to log into surveycto
    - dir_path: local folder path where attachments should be saved
    - dir_box_id: box id of folder where attachments shoud be saved (choose one of these two options)
    - encryption_key: path to encryption_key in case surveycto server is encrypted
    '''

    valid_destination = validate_destination(dir_path = dir_path, dir_box_id=dir_box_id)

    if valid_destination is False:
        print(f'Not valid destination')
        return

    if get_file_extension(survey_entries_file)=='.csv':
        download_attachments_from_csv(
                                attachment_columns=attachment_columns,
                                username=username,
                                password=password,
                                survey_entries_file=survey_entries_file,
                                servername=servername,
                                formid=formid,
                                dir_path=dir_path,
                                dir_box_id=dir_box_id,
                                encryption_key=None)


    if get_file_extension(survey_entries_file)=='.json':
        download_attachments_from_json(
                                attachment_columns=attachment_columns,
                                username=username,
                                password=password,
                                survey_entries_file=survey_entries_file,
                                dir_path=dir_path,
                                dir_box_id=dir_box_id,
                                encryption_key=None)
