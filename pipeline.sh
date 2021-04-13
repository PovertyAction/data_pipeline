#!/bin/bash

#0. How to run:
#./pipeline.sh --server labelremittance --form_id covid_endline_household --start_timestamp 0 --username "falamos@poverty-action.org" --password "mypassword" --columns_with_attachments "audio_audit_survey,comments,text_audit,sstrm_conversation,sstrm_sound_level" --outputs_path "/mnt/x/Box/CP_Projects/IPA_PHL_Projects/Labeled Remittances/COVID study/Data/endline_all" --server_key "/mnt/x/Box/CP_Projects/IPA_PHL_Projects/Labeled Remittances/COVID study/Questionnaire & programming/Programming/key/covid_endline_PRIVATEDONOTSHARE.pem"

#1. Get user paramenters
while [ $# -gt 0 ]; do
   if [[ $1 == *"--"* ]]; then
        param="${1/--/}"
        declare $param="$2"
   fi
  shift
done

#Expecting: $server $form_id $start_timestamp $username $password $columns_with_attachments $server_key $ouputs_path

#2. Build url
url="https://${server}.surveycto.com/api/v2/forms/data/wide/json/${form_id}?date=${start_timestamp}"

#3. Build local folder for json file
json_outputs_folder="data/${server}_${form_id}"
mkdir ${json_outputs_folder}

#4. Build json file path
timestamp_now=$(date +"%s")
file_name="${server}_${form_id}_${start_timestamp}_${timestamp_now}"
json_file_path="${json_outputs_folder}/${file_name}.json"

#5.Download main database. Check if server key was provided
if [ -z "${server_key}" ];
then
  curl -u "${username}:${password}" -o ${json_file_path} ${url}
else
  echo 'Using private key in curl request'
  echo $server_key
  curl -u "${username}:${password}" -F 'private_key=@"'"$server_key"'"' -o ${json_file_path} ${url}
fi
echo ${json_file_path}
echo 'Fist 100 chars:'
head -c 100 ${json_file_path}
echo ''

#6.Transform to .csv. Build folder for outputs
outputs_folder="${outputs_path}/${server}_${form_id}"
mkdir "${outputs_folder}"
echo 'Creating csv'
echo ${json_file_path}
echo ${outputs_folder}
python3 file_parser.py "${json_file_path}" "${outputs_folder}"

#7.Download attachments. Check if server key was provided
echo ${columns_with_attachments}
media_folder="${outputs_path}/media"
mkdir "${media_folder}"


if [ -z "${server_key}" ];
then
  python3 surveycto_data_downloader.py "${json_file_path}" "${media_folder}" "${username}" "${password}" "${columns_with_attachments}"
else
  echo 'Using private key to download attachments'
  python3 surveycto_data_downloader.py "${json_file_path}" "${media_folder}" "${username}" "${password}" "${columns_with_attachments}" "${server_key}"
fi
