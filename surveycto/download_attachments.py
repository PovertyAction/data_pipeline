import argparse
import sys
sys.path.append(os.path.dirname(__file__))
import surveycto_manager



def parse_args():
    """ Parse command line arguments.
    """
    parser = argparse.ArgumentParser(description="Surveycto attachments downloader")

   survey_entries_file_name = sys.argv[1]
   attachment_columns = sys.argv[2].split(',')
   username = sys.argv[3]
   password=sys.argv[4]
   encryption_key = sys.argv[6]
   encryption_key=encryption_key
   dir_path=None,
   dir_box_id=None,

    #Add arguments
    for (argument, arg_help, arg_type, arg_required) in [
           ('--survey_file', 'survey_file', str, True),
           ('--attachment_columns', 'attachment_columns comma separated', str, True),
           ('--username', 'surveycto username',str, True),
           ('--password','surveycto password', str, True),
           ('--encryption_key','path to encryption_key',str, False),
           ('--dest_path','dest_path',str, False),
           ('--dest_box_id','dest_box_id',str, False)]:

        parser.add_argument(
            argument,
            help=arg_help,
            default=None,
            required=arg_required,
            type=arg_type
        )

    return parser.parse_args()



if __name__ == '__main__':

    args = parse_args()

    surveycto_manager.download_attachments(
        survey_entries_file=args.survey_file,
        attachment_columns=args.attachment_columns,
        username=args.username,
        password=args.password,
        encryption_key=argss.encryption_key,
        dir_path=args.dest_path,
        dir_box_id=args.dest_box_id
    )
