#Reference
#http://opensource.box.com/box-python-sdk/
#http://opensource.box.com/box-python-sdk/tutorials/intro.html
#https://github.com/box/box-python-sdk/blob/master/docs/usage
import ntpath
import box_credentials

from boxsdk import Client, OAuth2

oauth = OAuth2(
  client_id= box_credentials.get_client_id(),
  client_secret=box_credentials.get_client_secret(),
  access_token=box_credentials.get_developer_token()
)
client = Client(oauth)

#https://github.com/box/box-python-sdk/blob/master/docs/usage/folders.md#get-the-items-in-a-folder
def get_list_files(box_folder_id):
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

def upload_file(box_folder_id, file_path):

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
