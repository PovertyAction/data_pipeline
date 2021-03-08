import ijson
import pandas as pd
import os
import sys
import requests

import surveycto_credentials

def download_attachments(json_filename, attachment_columns):

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

                    file_name = 'attachments/'+value.split('/')[-1]

                    #Download file if it doesnt exist already
                    if os.path.isfile(file_name):
                        print(f'{file_name} already downloaded')
                        continue

                    #Send request
                    headers = {'X-OpenRosa-Version': '1.0'}
                    auth_basic = requests.auth.HTTPBasicAuth(
                        username=surveycto_credentials.get_username(), password=surveycto_credentials.get_password())

                    response = requests.get(value,
                                            headers= headers,
                                            auth= auth_basic)

                    #Save response content in file
                    data = response.content

                    f = open(file_name, 'wb')
                    f.write(data)
                    f.close()
                    print(f'{file_name} succesfully downloaded and saved')



if __name__ == '__main__':
    # json_file = sys.argv[1]
    json_file = 'mask_data_wide_complete.json'
    attachment_columns = ['text_audit']
    download_attachments(json_file, attachment_columns)
