#Reference
#http://opensource.box.com/box-python-sdk/
#http://opensource.box.com/box-python-sdk/tutorials/intro.html
#https://github.com/box/box-python-sdk/blob/master/docs/usage
import ntpath
import sys
import os
from boxsdk import Client, OAuth2, JWTAuth
import pathlib
import box_credentials

#https://github.com/box/box-python-sdk/blob/master/docs/usage/folders.md#get-the-items-in-a-folder
def get_list_files(auth_method, box_folder_id):

    client = get_box_client(auth_method)
    print(client)

    list_files = []

    try:
        items = client.folder(folder_id=str(box_folder_id)).get_items()
    except Exception as e:
        print("An exception occurred")
        print(e)
        return False

    for item in items:
        list_files.append(item.name)
    print(f'Finished getting list files. Amount files: {len(list_files)}')
    return list_files

def get_file_extension(file_path, include_dot):
    split_tup = os.path.splitext(file_path)
    file_extension = split_tup[1]
    print(file_extension)

    if include_dot:
        return file_extension
    else:
        return file_extension[1:]

def check_file_exists_in_folder(auth_method, box_folder_id, file_name):

    client = get_box_client(auth_method)

    # https://github.com/box/box-python-sdk/blob/main/docs/usage/search.md#search-for-content
    # https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.search.Search.query

    box_folder = client.folder(folder_id=box_folder_id)

    items = client.search().query(query=file_name,
                                    limit=1,
                                    file_extensions=[get_file_extension(file_name, include_dot=False)],
                                    ancestor_folders=[box_folder],
                                    type='file',
                                    content_types='name')
    for item in items:
        if item.name == file_name:
            print('The item ID is {0} and the item name is {1}'.format(item.id, item.name))
            #If found one, return true
            return True

    #If did not find any, return false
    return False

def upload_file(auth_method, box_folder_id, file_path):

    client = get_box_client(auth_method)

    try:
        box_folder = client.folder(folder_id=box_folder_id)
        file_name = ntpath.basename(file_path)
        uploaded_file = box_folder.upload(file_path=file_path, file_name=file_name)

        if uploaded_file:
            print(f'{file_path} succesfully uploaded to Box')
            return True
        else:
            raise Exception(f'Error uploading {file_path} to box folder {box_folder_id}')

    except Exception as e:
        print("An exception occurred")
        raise Exception(e)

def get_box_client(authentication_method):
    if authentication_method == 'oauth':
        oauth = OAuth2(
          client_id= box_credentials.get_client_id(),
          client_secret = box_credentials.get_client_secret(),
          access_token = box_credentials.get_developer_token()
        )
        client = Client(oauth)
        return client
    elif authentication_method == 'jwt':
        jwt_config_file_name = box_credentials.get_jwt_config_file_name()

        jwt_config_file_path = os.path.join(pathlib.Path(__file__).parent.absolute(),jwt_config_file_name)

        config = JWTAuth.from_settings_file(jwt_config_file_path)
        client = Client(config)

        #When auth with jwt, client is a service user. We need to get access to ipa box account with access to folders
        #Reference: https://github.com/box/box-python-sdk/blob/main/docs/usage/authentication.md#server-auth-with-jwt
        service_user = client.user(box_credentials.get_ipa_box_account_user_id())
        return client.as_user(service_user)


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



if __name__ == '__main__':

    print(check_file_exists_in_folder(auth_method='jwt', box_folder_id='139879419741', file_name='AA_5c6ca838-4a3c-459f-a4c3-5f2df9665d89_telefono1.m4a'))
