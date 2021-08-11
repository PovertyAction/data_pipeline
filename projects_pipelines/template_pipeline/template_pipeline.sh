#!/bin/bash

: '

How to run:

./template_pipeline.sh \
--server bdmaskrct \
--download_wide_csv False \
--download_wide_json True \
--transform_json_to_csv True \
--form_id mask_monitoring_form_bn \
--start_timestamp 0 \
--username "researchsupport@poverty-action.org" \
--password "pass!" \
--box_path "./box_path_simulation/" \
--box_folder_id 139653613903 \
--s3_bucket mask-monitoring-project \
--columns_with_attachments "colA,colB" \
--media_box_path "./box_path_simulation/media" \
--media_box_folder_id 139653613903 \
--server_key_file_id "824680196213"

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

#Build local folder for file
outputs_folder="data/${server}/${form_id}"
mkdir -p ${outputs_folder}
echo "Will save outputs in: ${outputs_folder}"
echo ''

#Download surveycto server key
if ! [ -z "${server_key_file_id}" ];
then
  server_key="${outputs_folder}/server_key.pem"
  python3 ../../box/download_from_box.py "${server_key_file_id}" "${server_key}"
  echo 'Servey key downloaded'
else
  server_key=''
fi

#1st argument is csv or json
download_survey_entries()
{
  format=$1

  #Build url to download survey entries
  if [ "$format" == "json" ];
  then
    url="https://${server}.surveycto.com/api/v2/forms/data/wide/json/${form_id}?date=${start_timestamp}"
  elif [ "$format" == "csv" ];
  then
    url="https://${server}.surveycto.com/api/v1/forms/data/wide/csv/${form_id}?date=${start_timestamp}"
  fi
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

#Download survey entries
FILES_DOWNLOADED=""
if [ "$download_wide_csv" == "True" ];
then
    download_survey_entries csv $server_key
    FILES_DOWNLOADED=$(echo "$file_path")
fi

if [ "$download_wide_json" == "True" ];
then
    download_survey_entries json $server_key

    #Add new file path to FILES_DOWNLOADED LIST
    if [ "$FILES_DOWNLOADED" == "" ];
    then
      FILES_DOWNLOADED=$(echo "$file_path")
    else
      FILES_DOWNLOADED+=$(echo " $file_path")
    fi

    #Transform to .csv.
    if [ "$transform_json_to_csv" == "True" ];
    then
      parsed_csv_file_path="$(echo "$file_path" | cut -f 1 -d '.')_parsed.csv"
      python3 ../../files_transformations/json_to_csv_parser.py "${file_path}" "${parsed_csv_file_path}"
      echo "Parsed csv created"
      echo "${parsed_csv_file_path}"
      FILES_DOWNLOADED+=$(echo " $parsed_csv_file_path")
      echo ''
    fi
fi
echo 'Survey entries downloaded'
echo "$FILES_DOWNLOADED"

#Upload every output file to box drive, box cloud or aws
for FILE in ${FILES_DOWNLOADED}
do
  #Copy file to box_path if box_path is not empty
  if ! [ -z "${box_path}" ];
  then
    cp "${FILE}" "${box_path}/."
    echo "${FILE} pushed to ${box_path} folder"
    echo ''
  fi

  #Copy file to box
  if ! [ -z "${box_folder_id}" ];
  then
    python3 ../../box/upload_to_box.py "${box_folder_id}" "${FILE}"
    echo "${FILE} pushed to ${box_folder_id} in box.com"
    echo ''
  fi

  #Copy file to aws
  if ! [ -z "${s3_bucket}" ];
  then
    python3 ../../aws/upload_to_s3.py "${FILE}" "${s3_bucket}"
    echo "${FILE} pushed to aws ${s3_bucket} bucket"
    echo ''
  fi
done

#Download attachments (also to box path, box directly or aws)
if ! [ -z "${columns_with_attachments}" ];
then

  #Create key where to save media files in s3 bucket
  s3_bucket_path_media="${outputs_folder}/media"

  python3 ../../surveycto/download_attachments.py --survey_file "${file_path}" --attachment_columns "${columns_with_attachments}" --username "${username}" --password "${password}" --encryption_key "${server_key}" --dest_path "${media_box_path}" --dest_box_id "${media_box_folder_id}" --s3_bucket "${s3_bucket}" --s3_bucket_path_media "${s3_bucket_path_media}"
  echo "Attachements downloaded"
  echo ''
fi
