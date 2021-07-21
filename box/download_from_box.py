import sys
import os
sys.path.append(os.path.dirname(__file__))
import box_manager

if __name__ == '__main__':

    file_id = sys.argv[1]
    file_path = sys.argv[2]

    box_manager.download_file(file_id, file_path)
