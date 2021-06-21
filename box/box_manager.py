#Reference
#http://opensource.box.com/box-python-sdk/
#http://opensource.box.com/box-python-sdk/tutorials/intro.html
#https://github.com/box/box-python-sdk/blob/master/docs/usage
import ntpath
import box_credentials
import sys

from boxsdk import Client, OAuth2, JWTAuth

#https://github.com/box/box-python-sdk/blob/master/docs/usage/folders.md#get-the-items-in-a-folder
def get_list_files(auth_method, box_folder_id):

    client = get_box_client(auth_method)

    list_files = []
    try:
        items = client.folder(folder_id=box_folder_id).get_items()
    except Exception as e:
        print("An exception occurred")
        print(e)
        return False

    for item in items:
        list_files.append(item.name)
    return list_files

def upload_file(auth_method, box_folder_id, file_path):

    client = get_box_client(auth_method)

    print('e')

    try:
        box_folder = client.folder(folder_id=box_folder_id)
        file_name = ntpath.basename(file_path)
        uploaded_file = box_folder.upload(file_path=file_path, file_name=file_name)

        if uploaded_file:
            return True
        else:
            print(f'Error uploading {file_path} to box folder {box_folder_id}')
            return False

    except Exception as e:
        print("An exception occurred")
        print(e)
        return False

def get_box_client(authentication_method):
    if authentication_method == 'oauth':
        oauth = OAuth2(
          client_id= box_credentials.get_client_id(),
          client_secret = box_credentials.get_client_secret(),
          access_token = box_credentials.get_developer_token()
        )
        client = Client(oauth)
    elif authentication_method == 'jwt':
        jwt_config_file_path = box_credentials.get_jwt_config_file_path()
        print(jwt_config_file_path)
        config = JWTAuth.from_settings_file(jwt_config_file_path)
        client = Client(config)

    return client

if __name__ == '__main__':
    function = sys.argv[1]
    auth_method = sys.argv[2]
    box_folder_id = sys.argv[3]

    if len(sys.argv)>4 and function == 'upload_file':
        file_path = sys.argv[4]
        upload_file(auth_method, box_folder_id, file_path)

    elif function == 'get_list_files':
        print(get_list_files(auth_method, box_folder_id))

#Reference:
#https://developer.box.com/guides/uploads/chunked/#:~:text=The%20Chunked%20Upload%20API%20provides,a%20failed%20request%20more%20reliably.
#https://developer.box.com/guides/uploads/chunked/with-sdks/

#https://github.com/box/box-python-sdk/blob/master/docs/usage/files.md#chunked-upload
def upload_in_chuncks(box_folder_id, file_path):
    file_id = ''
    chunked_uploader = client.folder(box_folder_id).get_chunked_uploader(file_path) #.file(folder_id)??

    try:
        uploaded_file = chunked_uploader.start()
    except:
        uploaded_file = chunked_uploader.resume()

    print('File "{0}" uploaded to Box with file ID {1}'.format(uploaded_file.name, uploaded_file.id))
