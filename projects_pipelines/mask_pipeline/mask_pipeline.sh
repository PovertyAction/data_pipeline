#!/bin/bash

#How to run:
#./mask_pipeline.sh --server bdmaskrct --form_id mask_monitoring_form_bn --repeat_group ind_group --start_timestamp 0 --username "mali@poverty-action.org" --password "password"

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
outputs_folder="data/${server}/${form_id}"
mkdir -p ${outputs_folder}

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
  curl -u "${username}:${password}" -F 'private_key=@"'"$server_key"'"' -o ${parent_file_name} ${parent_url}
  curl -u "${username}:${password}" -F 'private_key=@"'"$server_key"'"' -o ${repeatgroup_file_name} ${repeatgroup_url}
fi

#6. Clean and merge files
csv_merged_file_path="${outputs_folder}/${server}_${form_id}.csv"
python3 masks_clean_and_merge.py "${parent_file_name}" "${repeatgroup_file_name}" "${csv_merged_file_path}" "${server}_${form_id}"

#7. Transform all bangladesh csv files to one json
json_merged_file_path="${outputs_folder}/${server}_${form_id}.json"
selected_keys="status-mask,status-distance,status-agegroup,status-gender,timestamp,uid,intro_group-area,district_group-ward_village,gps-Latitude,gps-Longitude,gps-Accuracy,intro_group-division,intro_group-district,intro_group-upazila,intro_group-union"

python3 ../../files_transformations/csv_to_filtered_json.py "${csv_merged_file_path}" "${json_merged_file_path}" "${selected_keys}"

#8. Upload csv and json to aws s3 bucket
s3_bucket="mask-monitoring-project"
python3 ../../aws/upload_to_s3.py "${csv_merged_file_path}" "${s3_bucket}"
python3 ../../aws/upload_to_s3.py "${json_merged_file_path}" "${s3_bucket}"

#9. Generate presigned url to download data
python3 ../aws/generate_s3_presigned_url.py "${s3_bucket}" "${server}_${form_id}.csv"
python3 ../aws/generate_s3_presigned_url.py "${s3_bucket}" "${server}_${form_id}.json"
