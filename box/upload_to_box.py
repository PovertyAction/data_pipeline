import sys
import os
sys.path.append(os.path.dirname(__file__))
import box_manager

if __name__ == '__main__':

    arg_auth_method = 'jwt'
    arg_box_folder_id = sys.argv[1]
    arg_file_path = sys.argv[2]

    box_manager.upload_file(arg_auth_method, arg_box_folder_id, arg_file_path)
