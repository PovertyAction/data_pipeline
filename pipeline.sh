#!/bin/bash
'''
1. Launch ec2 instance

2. Log into instance
ssh -i /aws-key-pair.pem ubuntu@ec2-3-15-202-166.us-east-2.compute.amazonaws.com #Yes to confirmation.

3. Download repo
git clone https://github.com/PovertyAction/surveycto_data_download.git

4. Install dependencies

sudo apt update
sudo apt install python3-pip #Add yes confirmation

cd surveycto_data_download

If venv desired
`python3 -m venv venv`
`source venv/bin/activate`

`pip3 install -r requirements.txt`

5. Create tmux session
tmux new -s data_download
'''

#Activate venv
#. ./venv/bin/activate

#Get user paramenters
while [ $# -gt 0 ]; do
   if [[ $1 == *"--"* ]]; then
        param="${1/--/}"
        declare $param="$2"
   fi
  shift
done
#Expecting: $server $form_id $start_timestamp $username $password $columns_with_attachments $server_key

#Build url
url="https://${server}.surveycto.com/api/v2/forms/data/wide/json/${form_id}?date=${start_timestamp}"

#Build folder for outputs
outputs_folder="${server}_${form_id}"
mkdir ${outputs_folder}

#Build json file path
timestamp_now=$(date +"%s")
file_name="${server}_${form_id}_${start_timestamp}_${timestamp_now}"
json_file_path="${outputs_folder}/${file_name}.json"

#Download main database. Check if server key was provided
if [ -z "${server_key}" ]; #server_key is unset or set to empty string
then
  curl -u "${username}:${password}" -o ${json_file_path} ${url}
else
  echo 'Using private key in curl request'
  echo $server_key
  # printf -v private_key_string -- 'private_key=@%s' \ "$server_key"
  # echo $private_key_string
  # curl -u "${username}:${password}" -F '"$private_key_string"' -o ${json_file_path} ${url}
  curl -u "${username}:${password}" -F 'private_key=@"'"$server_key"'"' -o ${json_file_path} ${url}
  # curl -u "${username}:${password}" -F 'private_key=@/mnt/x/Box/CP_Projects/IPA_PHL_Projects/Labeled Remittances/COVID study/Questionnaire & programming/Programming/key/covid_endline_PRIVATEDONOTSHARE.pem' -o ${json_file_path} ${url}
fi
echo ${json_file_path}
echo 'Fist 100 chars:'
head -c 100 ${json_file_path}

#2.Transform to .csv
python3 file_parser.py ${json_file_path} ${outputs_folder}


echo ${columns_with_attachments}
#3.Download attachments
media_folder="${outputs_folder}/media"
mkdir ${media_folder}
python3 surveycto_data_downloader.py ${json_file_path} ${media_folder} ${username} ${password} ${columns_with_attachments}
