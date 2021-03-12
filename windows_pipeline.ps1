#How to run:
#.\windows_pipeline.ps1 -servername bdmaskrct -form_id maskrct_phone_followup -start_timestamp 1615550000 -username mali@poverty-action.org -password GRDSgrds! -dir_path "X:\\Box\\Mask_data"                  

#Get user parameters
param ($servername, $form_id, $start_timestamp, $username, $password, $dir_path)

#Build url
$url="https://${servername}.surveycto.com/api/v2/forms/data/wide/json/${form_id}?date=${start_timestamp}"
write-host $url

#Build main database file path
$timestamp_now=[int][double]::Parse((Get-Date -UFormat %s))
$file_path="${dir_path}/${servername}_${form_id}_${start_timestamp}_${timestamp_now}.json"
write-host $file_path

#1.Download main dataset
curl.exe -u "${username}:${password}" -o ${file_path} ${url}

#2.Transform to .csv
python file_parser.py ${file_path}

#3.Download attachments
$media_path="${dir_path}/media"
python surveycto_data_downloader.py ${file_path} ${media_path} ${username} ${password}
