#!/bin/bash

#How to run:
#./mask_pipeline.sh --server bdmaskrct --form_id mask_monitoring_form_bn --repeat_group ind_group --start_timestamp 0 --username "mali@poverty-action.org" --password "password"

#PENDINGS:
# 1.git pull changes in stata and python file
# 2.cleaning should be different for different forms
# 3.install stata in server
# 4.merge json files for bangladesh gov.
# 5.give emily and islamul access

#0. Get new version from git if changes have occured in scripts that this pipeline runs (ex, python or stata cleaning files)
#->git pull origin master

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
outputs_folder="data"
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
csv_merged_file_path="${outputs_folder}/${server}_${form_id}.csv"
python3 clean_and_merge.py "${parent_file_name}" "${repeatgroup_file_name}" "${csv_merged_file_path}"

#->Incremental downloads pending too. Not necessary but would be good.

#6b. Clean with stata
#->stata more_clening.do "csv_merged_file_path". The problem with this one is feasibility of loading all data in stata

#7. Transform all bangladesh csv files to one json
json_merged_file_path="${outputs_folder}/${server}_${form_id}.json"
python3 csv_to_filtered_json.py "${csv_merged_file_path}" "${json_merged_file_path}"

#8. Upload csv and json to aws s3 bucket
s3_bucket="mask-monitoring-project"
python3 upload_to_s3.py "${csv_merged_file_path}" "${s3_bucket}"
python3 upload_to_s3.py "${json_merged_file_path}" "${s3_bucket}"

#9. Generate presigned url to download data
python3 generate_s3_presigned_url.py "${s3_bucket}" "${server}_${form_id}.csv"
python3 generate_s3_presigned_url.py "${s3_bucket}" "${server}_${form_id}.json"
