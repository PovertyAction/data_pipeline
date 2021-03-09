import ijson
import pandas as pd
import os
import sys
import requests

import surveycto_credentials
import box_manager

def download_file_from_surveycto(file_url, file_path):

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

def download_attachments_and_upload_to_dropbox(json_filename, attachment_columns, box_folder_id):

    files_in_box = box_manager.get_list_files(box_folder_id)

    with open(json_filename, 'rb') as input_file:
        # load json iteratively
        parser = ijson.parse(input_file)

        rows_counter=0

        for prefix, event, value in parser:
            #Check if prefix we are reading is a json key
            if len(prefix.split('.'))>1:
                key = prefix.split('.')[1]

                #Check if key is associated to one with urls do download
                if key in attachment_columns:

                    #Get file_name
                    file_name = value.split('/')[-1]

                    #Check if file already exist in box. If it does, move to next one.
                    if file_name in files_in_box:
                        continue

                    #If not, download it, upload it to box and delete it

                    file_path = 'attachments/'+file_name

                    #Download file if it doesnt exist already
                    if os.path.isfile(file_path):
                        print(f'{file_path} already downloaded')
                    else:
                        download_file_from_surveycto(file_url=value, file_path=file_path)
                        print(f'{file_path} succesfully downloaded')

                    #Upload file to box
                    box_manager.upload_file(box_folder_id, file_path)

                    #Delete file from local
                    os.remove(file_path)



if __name__ == '__main__':
    # json_file = sys.argv[1]
    json_file = 'mask_data_wide_complete.json'
    attachment_columns = ['text_audit', 'audio_audit']
    box_folder_id = ''
    download_attachments_and_upload_to_dropbox(json_file, attachment_columns, box_folder_id)
