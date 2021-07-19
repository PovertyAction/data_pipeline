#!/bin/bash

: '

How to run:

Masks:

./template_pipeline.sh \
--server bdmaskrct \
--form_id mask_monitoring_form_bn \
--start_timestamp 1626295923 \
--username "mali@poverty-action.org" \
--password "pass!" \
--transform_to_csv "True" \
--box_path "./box_path_simulation/" \
--box_folder_id 139653613903 \
--s3_bucket mask-monitoring-project \
--columns_with_attachments "colA,colB" \
--media_box_path "./box_path_simulation/media" \
--media_box_folder_id 139653613903 \


Labelremittance:

./template_pipeline.sh \
--server labelremittance \
--form_id covid_endline_household \
--start_timestamp 0 \
--username "falamos@poverty-action.org" \
--password "pass" \
--transform_to_csv "False" \
--box_path "./box_path_simulation/" \
--box_folder_id 141543819347 \
--s3_bucket mask-monitoring-project \
--columns_with_attachments "audio_audit_survey,comments,text_audit,sstrm_conversation,sstrm_sound_level" \
--media_box_path "./box_path_simulation/media" \
--media_box_folder_id 141540328939 \
--server_key "path/to/key/key.pem"

hfs:

./template_pipeline.sh \
--server hfslatam \
--form_id hfslatam_560_Chile \
--start_timestamp 0 \
--username "falamos@poverty-action.org" \
--password "pass" \
--transform_to_csv "True" \
--box_path "./box_path_simulation/" \
--box_folder_id 141543819347 \
--s3_bucket mask-monitoring-project \
--columns_with_attachments "audit,text_audit" \
--media_box_path "./box_path_simulation/media" \
--media_box_folder_id 141540328939

'


#1. Get user paramenters
while [ $# -gt 0 ]; do
   if [[ $1 == *"--"* ]]; then
        param="${1/--/}"
        declare $param="$2"
   fi
  shift
done

#> Should do some arguments validations here, like checking certain arguments are not empy

#2. Build url to download survey entries
url="https://${server}.surveycto.com/api/v2/forms/data/wide/json/${form_id}?date=${start_timestamp}"
echo "Url to call: ${url}"
echo ''

#3. Build local folder for file
outputs_folder="data/${server}/${form_id}"
mkdir -p ${outputs_folder}
echo "Will save outputs in: ${outputs_folder}"
echo ''

#4. Build json file path
timestamp_now=$(date +"%s")
file_name="${server}_${form_id}_${start_timestamp}_${timestamp_now}"
json_file_path="${outputs_folder}/${file_name}.json"
echo "json file path: ${json_file_path}"
echo ''

# 5.Download main database. Check if server key was provided
if [ -z "${server_key}" ];
then
  curl -u "${username}:${password}" -o ${json_file_path} ${url}
else
  echo 'Using private key in curl request'
  echo $server_key
  curl -u "${username}:${password}" -F 'private_key=@"'"$server_key"'"' -o ${json_file_path} ${url}
fi
echo "${json_file_path} downloaded"
echo 'Fist 100 chars:'
head -c 100 ${json_file_path}
echo ''

#Check if there was an error in the download process, if yes, stop
#Identify error with "{"error" in the first chars of json_file_path
first_8_chr=$(head -c 8 ${json_file_path})
error_str='{"error"'
if [ "$first_8_chr" = "$error_str" ]; then
  echo "Error when downloading database, finishing pipeline"
  rm ${json_file_path}
  exit 0
fi

#6.Transform to .csv.
if [ "$transform_to_csv" == "True" ];
then
  csv_file_path="${outputs_folder}/${file_name}.csv"
  python3 ../../files_transformations/json_to_csv_parser.py "${json_file_path}" "${csv_file_path}"
  echo "${csv_file_path} created"
  echo ''

  FILES_TO_UPLOAD=$(echo "$json_file_path $csv_file_path")
else
  FILES_TO_UPLOAD=$(echo "$json_file_path")
fi
echo "FILES_TO_UPLOAD: ${FILES_TO_UPLOAD}"
echo ''


#Upload every output file to box drive, box cloud or aws
for FILE in ${FILES_TO_UPLOAD}
do
  #7. Copy file to box_path if box_path is not empty
  if ! [ -z "${box_path}" ];
  then
    cp "${FILE}" "${box_path}/."
    echo "${FILE} pushed to ${box_path} folder"
    echo ''
  fi

  #8. Copy file to box
  if ! [ -z "${box_folder_id}" ];
  then
    python3 ../../box/upload_to_box.py "${box_folder_id}" "${FILE}"
    echo "${FILE} pushed to ${box_folder_id} in box.com"
    echo ''
  fi

  #9. Copy file to aws
  if ! [ -z "${s3_bucket}" ];
  then
    python3 ../../aws/upload_to_s3.py "${FILE}" "${s3_bucket}"
    echo "${FILE} pushed to aws ${s3_bucket} bucket"
    echo ''
  fi
done

json_file_path="data/hfslatam/hfslatam_560_Chile/hfslatam_hfslatam_560_Chile_0_1626731876.json"

# 10.Download attachments (also to box path, box directly or aws)
if ! [ -z "${columns_with_attachments}" ];
then
  python3 ../../surveycto/download_attachments.py --survey_file "${json_file_path}" --attachment_columns "${columns_with_attachments}" --username "${username}" --password "${password}" --encryption_key "${server_key}" --dest_path "${media_box_path}" --dest_box_id "${media_box_folder_id}"
  echo "Attachements downloaded"
  echo ''
fi
