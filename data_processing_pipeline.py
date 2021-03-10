import surveycto_data_downloader
import file_parser
import sys

def run_pipeline(start_day_timespam, server_name, form_id, username, password, survey_entries_path_destination, media_path_destination):

    #1. Download main .json
    # survey_entries_file_name = 'X:\\Box Sync\\MASK Test folder\\bdmaskrct-maskrct_phone_followup-1615320826.json'
    survey_entries_file_name = surveycto_data_downloader.download_survey_entries(
        start_day_timespam=start_day_timespam,
        server_name=server_name,
        form_id=form_id,
        username=username,
        password=password,
        dir_where_to_save=survey_entries_path_destination
        )


    if survey_entries_file_name:

        #2. Transform main .json to .csv
        file_parser.parse_json_to_csv(survey_entries_file_name)


        #3. Download attachments
        attachment_columns = ['text_audit', 'audio_audit']
        surveycto_data_downloader.download_attachments(
            json_file = survey_entries_file_name,
            attachment_columns = attachment_columns,
            dir_path_where_save= media_path_destination,
            username=username,
            password=password)

if __name__ == '__main__':
    print(sys.argv)
    start_day_timespam = sys.argv[1]
    server_name = sys.argv[2]
    form_id = sys.argv[3]
    username=sys.argv[4]
    password=sys.argv[5]
    survey_entries_path_destination=sys.argv[6]
    media_path_destination=sys.argv[7]

    run_pipeline(start_day_timespam, server_name, form_id, username, password, survey_entries_path_destination, media_path_destination)
