#How to run:
#.\windows_pipeline.ps1 -server bdmaskrct -form_id maskrct_phone_followup -start_timestamp 0 -username mali@poverty-action.org -password mehrabs_password -columns_with_attachments text_audit,audio_audit -outputs_path "X:\Box\Mask VM all data\Mask_data"

#.\windows_pipeline.ps1 -server labelremittance -form_id covid_endline_household -start_timestamp 0 -username "falamos@poverty-action.org" -password "mypassword" -columns_with_attachments "audio_audit_survey,comments,text_audit,sstrm_conversation,sstrm_sound_level" -outputs_path "X:\Box\CP_Projects\IPA_PHL_Projects\Labeled Remittances\COVID study\Data\endline_all" -server_key "X:\Box\CP_Projects\IPA_PHL_Projects\Labeled Remittances\COVID study\Questionnaire & programming\Programming\key\covid_endline_PRIVATEDONOTSHARE.pem"


#1. Get user parameters
param ($server, $form_id, $start_timestamp, $username, $password, $columns_with_attachments, $server_key, $outputs_path)
echo $server, $form_id, $start_timestamp, $username, $password, $columns_with_attachments, $server_key, $outputs_path

#2.Build url
$url="https://${server}.surveycto.com/api/v2/forms/data/wide/json/${form_id}?date=${start_timestamp}"

#3. Build local folder for json file
$json_outputs_folder="data/${server}_${form_id}"
New-Item -ItemType Directory -Force -Path ${json_outputs_folder}

#4. Build json file path
$timestamp_now=[int][double]::Parse((Get-Date -UFormat %s))
$file_name=".\${server}_${form_id}_${start_timestamp}_${timestamp_now}"
$json_file_path="${json_outputs_folder}/${file_name}.json"

#5.Download main database. Check if server key was provided
echo "${url}"

if($server_key -eq $null){
   curl.exe -u "${username}:${password}" -o ${json_file_path} ${url}
}else {
   echo "Downloading with server private key"
   $private_key_text="private_key=@$server_key"
   curl.exe -u "${username}:${password}" -F "${private_key_text}" -o "${json_file_path}" "${url}"
}

#6.Transform to .csv
#$outputs_folder="${outputs_path}/${server}_${form_id}"
#New-Item -ItemType Directory -Force -Path ${outputs_folder}

#python file_parser.py ${json_file_path} ${outputs_folder}


#7.Download attachments. Check if server key is provided
$media_path="${outputs_path}\media"
New-Item -ItemType Directory -Force -Path ${media_path}

if($server_key -eq $null){
   python surveycto_data_downloader.py "${json_file_path}" "${media_path}" "${username}" "${password}" "${columns_with_attachments}"
}else {
   python surveycto_data_downloader.py "${json_file_path}" "${media_path}" "${username}" "${password}" "${columns_with_attachments}" "${server_key}"
}