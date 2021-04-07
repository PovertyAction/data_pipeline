# Setting up VM:

1. Launch AWS Lightsail VM
2. Install boxcryptor

Invoke-WebRequest -Uri https://www.boxcryptor.com/l/download-windows -OutFile Boxcryptor.msi

3. Install box drive

Invoke-WebRequest -Uri https://e3.boxcdn.net/box-installers/desktop/releases/win/Box-x64.msi -OutFile Box-x64.msi

4. Install python

Invoke-WebRequest -Uri https://www.python.org/ftp/python/3.9.4/python-3.9.4-amd64.exe -OutFile python-3.9.4-amd64.exe

5. Install git

Invoke-WebRequest -Uri https://github.com/git-for-windows/git/releases/download/v2.31.1.windows.1/Git-2.31.1-64-bit.exe -OutFile Git-2.31.1-64-bit.exe

6. Clone this repo

git clone https://github.com/PovertyAction/surveycto_data_download.git

7. Install dependencies (requirements.txt)

# Running pipeline:

chmod +x pipeline.sh

./pipeline.sh --server server --form_id form_id --start_timestamp start_timestamp --username username --password password --columns_with_attachments columns_with_attachments --server_key server_key

'''
python data_processing_pipeline.py '1615378426' 'bdmaskrct' 'maskrct_phone_followup' $env:SURVEYCTO_USERNAME $env:SURVEYCTO_PASSWORD 'X:\\Box Sync\\MASK Test folder' 'X:\\Box Sync\\MASK Test folder\\media
'''

to:

1. Download survey data in json format

```
curl -u "username:password" -o ~/mask_data.json https://bdmaskrct.surveycto.com/api/v2/forms/data/wide/json/maskrct_phone_followup?date=0




```

2. Transform data to .csv
3. Download attachments


dos2unix
