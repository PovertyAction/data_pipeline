import ijson
import pandas as pd
import os
import sys
import requests

import surveycto_credentials

def download_survey_entries(start_day_timespam, server_name = 'bdmaskrct', form_id = 'maskrct_phone_followup'):

    #Send request
    headers = {'X-OpenRosa-Version': '1.0'}
    auth_basic = requests.auth.HTTPBasicAuth(
        username=surveycto_credentials.get_username(), password=surveycto_credentials.get_password())

    url = f'https://{server_name}.surveycto.com/api/v2/forms/data/wide/json/{form_id}?date={start_day_timespam}'
    response = requests.get(url,
                            headers= headers,
                            auth= auth_basic)

    #Save response content in file
    data = response.content

    file_name = f'{server_name}-{form_id}-{start_day_timespam}.json'
    f = open(file_name, 'wb')
    f.write(data)
    f.close()
    print(f'{file_name} succesfully downloaded and saved')



if __name__ == '__main__':
    start_day_timespam = '1615320826'
    download_survey_entries(start_day_timespam)
