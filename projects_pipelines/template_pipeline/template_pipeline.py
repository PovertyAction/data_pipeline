# Replication of template_pipeline.sh in python

'''
python template_pipeline.py --server migrationsurvey --forms_ids "migration_midline_IP;migration_bc_IP;hh_survey_IP;migration_midline_tracking" --username researchsupport@poverty-action.org --password "password" --start_timestamp 0 --server_key_path "/mnt/c/Users/felip/surveycto_data_download/projects_pipelines/template_pipeline/data/migrationsurvey/hh_survey_IP/server_key.pem"
'''


import os
import argparse
import time

def parse_args():
    """ Parse command line arguments.
    """
    parser = argparse.ArgumentParser(description="Data Pipeline")

    #Add arguments
    for (argument, arg_help, arg_required) in [
           ('--server', 'server', True),
           ('--forms_ids', 'form_ids separated by ;', True),
           ('--cols_with_attachments', 'cols_with_attachments separated by ;', False),
           ('--username', 'username', True),
           ('--password', 'password', True),
           ('--start_timestamp', 'start_timestamp', True),
           ('--box_folder_id', 'box_folder_id', False),
           ('--media_box_folder_id', 'media_box_folder_id', False),
           ('--aws_bucket', 'aws_bucket', False),
           ('--server_key_path', 'server_key_path', False)
           ]:

        parser.add_argument(
            argument,
            help=arg_help,
            default=None,
            required=arg_required,
            type=str
        )

    return parser.parse_args()

def create_local_outputs_folder(server, form_id):

    outputs_folder=f'data/{server}/{form_id}'

    if not os.path.exists(outputs_folder):
        os.makedirs(outputs_folder)

    return outputs_folder

def build_raw_file_path(outputs_folder, server, form_id, start_timestamp, extension):


    timestamp_now = int(time.time())
    file_name = f'{server}_{form_id}_{start_timestamp}_{timestamp_now}.{extension}'
    file_path = os.path.join(outputs_folder, file_name)

    return file_path

def download_raw_json(server, form_id, start_timestamp, username, password, raw_json_path, server_key_path):

    #Build url
    url=f"https://{server}.surveycto.com/api/v2/forms/data/wide/json/{form_id}?date={start_timestamp}"

    #Build curl command
    if not server_key_path:
        curl_command = f"curl -u '{username}:{password}' -o {raw_json_path} {url}"
    else:
        curl_command = f"curl -u '{username}:{password}' -F 'private_key=@{server_key_path}' -o {raw_json_path} {url}"

    #Execute curl command
    print('Will run command:')
    print(curl_command)
    os.system(curl_command)



def run_pipeline(server,
                forms_ids,
                username,
                password,
                box_folder_id,
                start_timestamp,
                cols_with_attachments=None,
                aws_bucket=None,
                media_box_folder_id=None,
                server_key_path=None):

    #Download data for every form
    for form_index, form_id in enumerate(forms_ids):


        outputs_folder = create_local_outputs_folder(server, form_id)

        raw_json_path = build_raw_file_path(outputs_folder, server, form_id, start_timestamp, extension='json')

        raw_csv_path = build_raw_file_path(outputs_folder, server, form_id, start_timestamp, extension='csv')


        download_raw_json(server=server,
                                form_id=form_id,
                                start_timestamp=start_timestamp,
                                username=username,
                                password=password,
                                raw_json_path=raw_json_path,
                                server_key_path=server_key_path)

        # transform_json_to_csv(raw_json_path, raw_csv_path)
        #
        # upload_files_to_cloud(raw_csv_path, box_folder_id, aws_bucket)
        #
        # download_attachments()





if __name__ == '__main__':

    #Parse arguments
    args = parse_args()

    args_cols_with_attachments = None
    if args.cols_with_attachments:
        args_cols_with_attachments = args.cols_with_attachments.split(';')

    run_pipeline(server=args.server,
        forms_ids=args.forms_ids.split(';'),
        cols_with_attachments=args_cols_with_attachments,
        username=args.username,
        password=args.password,
        start_timestamp=args.start_timestamp,
        box_folder_id=args.box_folder_id,
        media_box_folder_id=args.media_box_folder_id,
        aws_bucket=args.aws_bucket,
        server_key_path=args.server_key_path)
