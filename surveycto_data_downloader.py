import ijson
import pandas as pd
import os
import sys
import requests
import ntpath
import time
import csv

sys.path.append('box')
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
        return True
    except Excepion as e:
        print("An exception occurred")
        print(e)
        return False

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
    print(f'Starting downoad of {file_url}')

    if dir_path_where_to_save:
        file_path = os.path.join(dir_path_where_to_save, file_name)

    #If files should be downloaded to box directly, we will download a local copy first, push to box and then delete
    elif box_folder_id:
        tmp_folder = os.path.join('data','tmp')
        #Create tmp folder if it does not exist
        if not os.path.exists(tmp_folder):
            os.makedirs(tmp_folder)
        file_path = os.path.join(tmp_folder, file_name)

    else:
        print('wtf')

    response = run_surveycto_api_download_request(file_url, username, password, encryption_key)

    #Check if error status code
    if response.status_code == 500:
        print(f'Error {response.status_code} when downloading {file_url}')
        print(response.text)
        return False

    #Save response content in file
    data = response.content

    f = open(file_path, 'wb')
    f.write(data)
    f.close()

    #If file was supposed to be saved locally, return file_path of downloaded file
    if dir_path_where_to_save:
        file_path

    #If file was supposed to be saved in box directly, push to box and delete local copy
    if box_folder_id:

       #Upload file to box
       upload_status = box_manager.upload_file('jwt', box_folder_id, file_path)
       if upload_status:
           print(f'{file_path} succesfully uploaded to Box')
       else:
           print(f'Error uploading {file_path} to Box. Moving to next one')
           return False

       #Delete file from local
       delete_status = safe_delete(file_path)
       if delete_status:
           print(f'{file_path} deleted from local')
           return True
       else:
           print(f'Error deleting {file_path}. Moving to next one')
           return False




def download_survey_entries(start_day_timespam, server_name, form_id, username, password, dir_where_to_save):

    file_url = f'https://{server_name}.surveycto.com/api/v2/forms/data/wide/json/{form_id}?date={start_day_timespam}'

    now_timespam = int(time.time())
    file_name = f'{server_name}-{form_id}-{start_day_timespam}_{now_timespam}.json'

    return download_file_from_surveycto(file_url=file_url,
                                    username=username,
                                    password=password,
                                    file_name=file_name,
                                    dir_path_where_to_save=dir_where_to_save)

def get_file_extension(file_path):
    split_tup = os.path.splitext(file_path)
    file_extension = split_tup[1]
    print(file_extension)
    return file_extension


def check_if_file_exists_or_download_it(file_name,
                                        files_already_downloaded,
                                        file_url,
                                        username,
                                        password,
                                        dir_path=None,
                                        dir_box_id=None,
                                        encryption_key=None):

    #Check if file has already been downloaded. If it does, move to next one.
    if file_name in files_already_downloaded:
        print(f'{file_name} already downloaded')
        return True

    #Else, proceed to download

    #Download file to local Or download to box directly (download local, push box, delete local)
    download_status = download_file_from_surveycto(
            file_url=file_url,
            username=username,
            password=password,
            file_name=file_name,
            dir_path_where_to_save=dir_path,
            box_folder_id=dir_box_id,
            encryption_key=encryption_key)

    if download_status:
        print(f'{file_name} succesfully downloaded')
        return True
    else:
        print(f'Error downloading {file_name} from SurveyCTO. Moving to next one')
        return False

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
                    check_if_file_exists_or_download_it(file_name=file_name,
                                                        files_already_downloaded=files_already_downloaded,
                                                        file_url=value,
                                                        username=username,
                                                        password=password,
                                                        dir_path=dir_path,
                                                        dir_box_id=dir_box_id)

def download_attachments_from_csv(attachment_columns,
                        username,
                        password,
                        survey_entries_file,
                        files_already_downloaded,
                        servername,
                        formid,
                        dir_path=None,
                        dir_box_id=None, encryption_key=None):


    print('eeee')
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

                    #Build file_url
                    uuid = row[header.index('KEY')]


                    if servername is None or formid is None:
                        raise ValueError('servername or formid is None')

                    file_url = f'https://{servername}.surveycto.com/api/v2/forms/{formid}/submissions/{uuid}/attachments/{file_name}'

                    check_if_file_exists_or_download_it(file_name=file_name,
                                                        files_already_downloaded=files_already_downloaded,
                                                        file_url=file_url,
                                                        username=username,
                                                        password=password,
                                                        dir_path=dir_path,
                                                        dir_box_id=dir_box_id)

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

    files_already_downloaded = get_list_files(dir_path = dir_path, dir_box_id=dir_box_id)

    if files_already_downloaded is False:
        print(f'Could not read files from folder destination')
        return
    else:
        print(f'N files found in folder destination: {len(files_already_downloaded)}')

    if get_file_extension(survey_entries_file)=='.csv':
        download_attachments_from_csv(
                                attachment_columns=attachment_columns,
                                username=username,
                                password=password,
                                survey_entries_file=survey_entries_file,
                                files_already_downloaded=files_already_downloaded,
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
                                dir_path=None,
                                dir_box_id=None,
                                encryption_key=None)



if __name__ == '__main__':
    print(sys.argv)
    survey_entries_file_name = sys.argv[1]
    media_path_destination = sys.argv[2]
    username = sys.argv[3]
    password=sys.argv[4]
    attachment_columns = sys.argv[5].split(',')

    if len(sys.argv)>6:
        encryption_key = sys.argv[6]
    else:
        encryption_key = False

    print(f'attachment_columns: {attachment_columns}')
    download_attachments(
        json_file = survey_entries_file_name,
        attachment_columns = attachment_columns,
        dir_path_where_save= media_path_destination,
        username=username,
        password=password,
        encryption_key=encryption_key)


# python .\surveycto_data_downloader.py .\data\labelremittance_covid_endline_household\labelremittance_covid_endline_household_0_1620760470.json "X:\Box\CP_Projects\IPA_PHL_Projects\Labeled Remittances\COVID study\Data\endline_all\media" "falamos@poverty-action.org" "password" "audio_audit_survey,comments,text_audit,sstrm_conversation,sstrm_sound_level" "X:\Box\CP_Projects\IPA_PHL_Projects\Labeled Remittances\COVID study\Questionnaire & programming\Programming\key\covid_endline_PRIVATEDONOTSHARE.pem"
