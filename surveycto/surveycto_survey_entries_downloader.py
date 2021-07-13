import os
import suveycto_data_downloader
import time

def download_survey_entries(start_day_timespam, server_name, form_id, username, password, dir_where_to_save):

    file_url = f'https://{server_name}.surveycto.com/api/v2/forms/data/wide/json/{form_id}?date={start_day_timespam}'

    now_timespam = int(time.time())
    file_path_where_save = os.path.join(dir_where_to_save,f'{server_name}-{form_id}-{start_day_timespam}_{now_timespam}.json')

    return suveycto_data_downloader.download_file_from_surveycto(file_url, file_path_where_save, username, password)
