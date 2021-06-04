#!/bin/bash

#How to run:
#./mask_pipeline.sh --server bdmaskrct --form_id mask_monitoring_form_bn --repeat_group ind_group --start_timestamp 0 --username "mali@poverty-action.org" --password "password" --server_key "C:/path/to/server/key"

#1. Get user paramenters
while [ $# -gt 0 ]; do
   if [[ $1 == *"--"* ]]; then
        param="${1/--/}"
        declare $param="$2"
   fi
  shift
done

#2. Build url to download long .csv files
parent_url="https://${server}.surveycto.com/api/v1/forms/data/csv/${form_id}"
repeatgroup_url="https://${server}.surveycto.com/api/v1/forms/data/csv/${form_id}/${repeat_group}"

#3. Build local folder for downloads
outputs_folder="data/${server}_${form_id}"
mkdir ${outputs_folder}

#4. Build file paths
timestamp_now=$(date +"%s")
parent_file_name="${outputs_folder}/${server}_${form_id}_${start_timestamp}_${timestamp_now}.csv"
repeatgroup_file_name="${outputs_folder}/${server}_${form_id}_${repeat_group}_${start_timestamp}_${timestamp_now}.csv"

#5.Download files. Check if server key was provided
if [ -z "${server_key}" ];
then
  curl -u "${username}:${password}" -o ${parent_file_name} ${parent_url}
  curl -u "${username}:${password}" -o ${repeatgroup_file_name} ${repeatgroup_url}
else
  echo 'Using private key in curl request'
  curl -u "${username}:${password}" -F 'private_key=@"'"$server_key"'"' -o ${parent_file_name} ${parent_url}
  curl -u "${username}:${password}" -F 'private_key=@"'"$server_key"'"' -o ${repeatgroup_file_name} ${repeatgroup_url}
fi

#6. Clean and merge files
csv_merged_file_path="${outputs_folder}/merged.csv"

python3 clean_and_merge.py "${parent_file_name}" "${repeatgroup_file_name}" "${merged_file_path}"

#7. Transform all bangladesh csv files to one json
json_merged_file_path="${outputs_folder}/merged.csv"
python3 csv_to_json.py "${csv_merged_file_path}" "${json_merged_file_path}"

#8. Upload csv and json to aws s3 bucket
s3_bucket="masks_data"
python3 upload_to_s3.py "${csv_merged_file_path}" "${s3_bucket}"
python3 upload_to_s3.py "${json_merged_file_path}" "${s3_bucket}"
