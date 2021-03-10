import ijson
import pandas as pd
import os
import sys
import requests
import ntpath

import surveycto_credentials
import box_manager

def download_file_from_surveycto(file_url, file_path):

    try:
        #Send request
        headers = {'X-OpenRosa-Version': '1.0'}
        auth_basic = requests.auth.HTTPBasicAuth(
         username=surveycto_credentials.get_username(), password=surveycto_credentials.get_password())

        response = requests.get(file_url,
                             headers= headers,
                             auth= auth_basic)

        #Save response content in file
        data = response.content

        f = open(file_path, 'wb')
        f.write(data)
        f.close()
        return True

    except Exception as e:
        print("An exception occurred")
        print(e)
        return False

def safe_delete(file_path):
    try:
        os.remove(file_path)
        return True
    except Excepion as e:
        print("An exception occurred")
        print(e)
        return False

def get_list_files(dir_path):
    if os.path.isdir(dir_path):
        only_files = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]
        return only_files
    else:
        print(f'{dir_path} is not a directory')
        return False

def download_attachments_and_upload_to_box_using_boxcryptor(json_file, attachment_columns, boxcryptor_folder_path):

    files_in_box = get_list_files(boxcryptor_folder_path)
    if files_in_box is False:
        print(f'Could not read files from folder {box_folder_id}')
    else:
        print(f'Files found in box folder {box_folder_id}: {files_in_box}')

    with open(json_filename, 'rb') as input_file:
        # load json iteratively
        parser = ijson.parse(input_file)
        for prefix, event, value in parser:
            #Check if prefix we are reading is a json key
            #We know json keys come in the shape "prefix.key"
            if len(prefix.split('.'))>1:
                key = prefix.split('.')[1]

                #Check if key is associated to one of columns with urls to download
                if key in attachment_columns and value !='':

                    #Get file_name
                    file_name = ntpath.basename(value)
                    print('---')
                    print(f'Working on {file_name}')

                    #Check if file already exist in box. If it does, move to next one.
                    if file_name in files_in_box:
                        print(f'{file_name} already in box, skipping')
                        continue

                    #Else, proceed to download to box via boxcryptor

                    #Download file to local if it doesnt exist already
                    file_path = os.path.join(boxcryptor_folder_path, file_name)

                    if os.path.isfile(file_path):
                        print(f'{file_path} already downloaded')
                    else:
                        download_status = download_file_from_surveycto(file_url=value, file_path=file_path)
                        if download_status:
                            print(f'{file_path} succesfully downloaded to boxcryptor folder')
                        else:
                            print(f'Error downloading {file_path} from SurveyCTO. Moving to next one')
                            continue



def download_attachments_and_upload_to_box_using_box_api(json_filename, attachment_columns, box_folder_id):

    files_in_box = box_manager.get_list_files(box_folder_id)
    if files_in_box is False:
        print(f'Could not read files from folder {box_folder_id}')
    else:
        print(f'Files found in box folder {box_folder_id}: {files_in_box}')

    with open(json_filename, 'rb') as input_file:
        # load json iteratively
        parser = ijson.parse(input_file)
        for prefix, event, value in parser:
            #Check if prefix we are reading is a json key
            #We know json keys come in the shape "prefix.key"
            if len(prefix.split('.'))>1:
                key = prefix.split('.')[1]

                #Check if key is associated to one of columns with urls to download
                if key in attachment_columns and value !='':

                    #Get file_name
                    file_name = ntpath.basename(value)
                    print('---')
                    print(f'Working on {file_name}')

                    #Check if file already exist in box. If it does, move to next one.
                    if file_name in files_in_box:
                        print(f'{file_name} already in box, skipping')
                        continue

                    #Else, proceed to download to local, upload to Box, delete from local

                    #Download file to local if it doesnt exist already
                    file_path = os.path.join('attachments',file_name)

                    if os.path.isfile(file_path):
                        print(f'{file_path} already downloaded')
                    else:
                        download_status = download_file_from_surveycto(file_url=value, file_path=file_path)
                        if download_status:
                            print(f'{file_path} succesfully downloaded to local')
                        else:
                            print(f'Error downloading {file_path} from SurveyCTO. Moving to next one')
                            continue

                    #Upload file to box
                    upload_status = box_manager.upload_file(box_folder_id, file_path)
                    if upload_status:
                        print(f'{file_path} succesfully uploaded to Box')
                    else:
                        print(f'Error uploading {file_path} to Box. Moving to next one')
                        continue

                    #Delete file from local
                    delete_status = safe_delete(file_path)
                    if delete_status:
                        print(f'{file_path} deleted from local')
                    else:
                        print(f'Error deleting {file_path}. Moving to next one')
                        continue


if __name__ == '__main__':
    # json_file = sys.argv[1]
    json_file = 'mask_data_wide_complete.json'
    attachment_columns = ['text_audit', 'audio_audit']
    box_folder_id = '133150240980'
    # download_attachments_and_upload_to_box_using_box_api(json_file, attachment_columns, box_folder_id)

    download_attachments_and_upload_to_box_using_boxcryptor(json_file, attachment_columns, boxcryptor_folder_path)
