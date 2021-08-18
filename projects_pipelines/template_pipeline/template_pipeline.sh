#!/bin/bash

: '

How to run:

./template_pipeline.sh \
--server migrationsurvey \
--form_ids migration_midline_IP;migration_bc_IP;hh_survey_IP;migration_midline_tracking \
--columns_with_attachments "text_audit,audio_hh_consent,audio_indiv_consent,audio_hh_head;text_audit;audio_hh_consent,audio_hh_head;text_audit" \
--start_timestamp 0 \
--username "researchsupport@poverty-action.org" \
--password "researchsupport_password" \
--box_folder_id "142713774640" \
--media_box_folder_id "142713042079" \
--server_key_file_id "844416889094"

Note: Not all inputs are necessary
Mandatory inputs: server, form_id, start_timestamp, username, password, box_path or box_folder_id

'

#Get user paramenters
while [ $# -gt 0 ]; do
  if [[ $1 == *"--"* ]]; then
    param="${1/--/}"
    declare $param="$2"
  fi
  shift
done

#> Pending: Should do some arguments validations here, like checking certain arguments are not empy and that others are valid

#Download surveycto server key
if ! [ -z "${server_key_file_id}" ];
then
  server_key="${outputs_folder}/server_key.pem"
  python3 ../../box/download_from_box.py "${server_key_file_id}" "${server_key}"
  echo 'Servey key downloaded'
else
  server_key=''
fi

#1st argument is form_id
download_survey_entries()
{
  form_id=$1

  #Build url to download survey entries
  url="https://${server}.surveycto.com/api/v2/forms/data/wide/json/${form_id}?date=${start_timestamp}"
  echo "Url to call: ${url}"
  echo ''

  #Build file path
  timestamp_now=$(date +"%s")
  file_name="${server}_${form_id}_${start_timestamp}_${timestamp_now}.${format}"
  file_path="${outputs_folder}/${file_name}"
  echo "file path: ${file_path}"
  echo ''

  #Download main database. Check if server key was provided
  if ! [ "$server_key" == "" ];
  then
    curl -u "${username}:${password}" -F 'private_key=@"'"$server_key"'"' -o ${file_path} ${url}
  else
    curl -u "${username}:${password}" -o ${file_path} ${url}
  fi

  #Prints
  echo "${file_path} downloaded"
  echo 'Fist 100 chars:'
  head -c 100 ${file_path}
  echo ''

  #Check if there was an error in the download process, if yes, stop
  first_8_chr=$(head -c 8 ${file_path})

  #Build string with error
  error_str='{"error"'
  if [ "$first_8_chr" = "$error_str" ];
  then
    echo 'Error when downloading database, finishing pipeline'
    rm ${file_path}
    exit 0
  fi
}

upload_files()
{

  files_to_upload=$1

  #Upload every output file to box drive, box cloud or aws
  for file in ${files_to_upload}
  do
    #Copy file to box_path if box_path is not empty
    if ! [ -z "${box_path}" ];
    then
      cp "${file}" "${box_path}/."
      echo "${file} pushed to ${box_path} folder"
      echo ''
    fi

    #Copy file to box
    if ! [ -z "${box_folder_id}" ];
    then
      python3 ../../box/upload_to_box.py "${box_folder_id}" "${file}"
      echo "${file} pushed to ${box_folder_id} in box.com"
      echo ''
    fi

    #Copy file to aws
    if ! [ -z "${s3_bucket}" ];
    then
      python3 ../../aws/upload_to_s3.py "${file}" "${s3_bucket}"
      echo "${file} pushed to aws ${s3_bucket} bucket"
      echo ''
    fi
  done
}

download_upload_attachments()
{
  columns_with_attachments=$1

  #Download attachments (also to box path, box directly or aws)
  if ! [ -z "${columns_with_attachments}" ];
  then

    #Create key where to save media files in s3 bucket
    s3_bucket_path_media="${outputs_folder}/media"

    python3 ../../surveycto/download_upload_attachments.py --survey_file "${file_path}" --attachment_columns "${columns_with_attachments}" --username "${username}" --password "${password}" --encryption_key "${server_key}" --dest_path "${media_box_path}" --dest_box_id "${media_box_folder_id}" --s3_bucket "${s3_bucket}" --s3_bucket_path_media "${s3_bucket_path_media}"
    echo "Attachements downloaded"
    echo ''
  fi

}

download_upload_forms_data()
{

  form_id=$1
  columns_with_attachments=$3

  #Build local folder for file
  outputs_folder="data/${server}/${form_id}"
  mkdir -p ${outputs_folder}
  echo "Will save outputs in: ${outputs_folder}"
  echo ''

  #Download survey entries in json format
  download_survey_entries $form_id

  #Parse json to csv
  parsed_csv_file_path="$(echo "$file_path" | cut -f 1 -d '.').csv"
  python3 ../../files_transformations/json_to_csv_parser.py "${file_path}" "${parsed_csv_file_path}"
  echo "Parsed csv created"
  echo "${parsed_csv_file_path}"

  #Upload files
  files_to_upload=$(echo "$file_path $parsed_csv_file_path")
  echo 'files_to_upload'
  echo "$files_to_upload"
  upload_files $files_to_upload

  #Download attachments
  download_attachments $columns_with_attachments

}

#Loop over each form and its att
