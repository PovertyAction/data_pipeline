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

#Get user parameters
SERVER="$1"
FORM_ID="$2"
START_TIMESPAM="$3"
USERNAME="$4"
PASSWORD="$5"
COLUMNS_WITH_ATTACHMENTS="$6"

#Build url
URL="https://${SERVER}.surveycto.com/api/v2/forms/data/wide/json/${FORM_ID}?date=${START_TIMESPAM}"

#Build folder for outputs
OUTPUTS_FOLDER="${SERVER}_${FORM_ID}"
mkdir ${OUTPUTS_FOLDER}

#Build json file path
TIMESTAMP_NOW=$(date +"%s")
FILE_NAME="${SERVER}_${FORM_ID}_${START_TIMESPAM}_${TIMESTAMP_NOW}"
JSON_FILE_PATH="${OUTPUTS_FOLDER}/${FILE_NAME}.json"

#Download main database
curl -u "${USERNAME}:${PASSWORD}" -o ${JSON_FILE_PATH} ${URL}
echo ${JSON_FILE_PATH}
echo 'Fist 100 chars:'
head -c 100 ${JSON_FILE_PATH}

#2.Transform to .csv
python3 file_parser.py ${FILE_PATH} ${DIR_PATH}

#3.Download attachments
python3 surveycto_data_downloader.py ${FILE_PATH} './media' ${USERNAME} ${PASSWORD}
