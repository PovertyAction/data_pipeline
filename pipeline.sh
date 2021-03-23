#!/bin/bash

#Activate venv
#. ./venv/bin/activate

#Get user parameters
SERVER="$1"
FORM_ID="$2"
START_TIMESPAM="$3"
USERNAME="$4"
PASSWORD="$5"
DIR_PATH="$6"
#Build url
URL="https://${SERVER}.surveycto.com/api/v2/forms/data/wide/json/${FORM_ID}?date=${START_TIMESPAM}"

#Build main database file path
TIMESTAMP_NOW=$(date +"%s")
FILE_PATH="${DIR_PATH}/${SERVER}_${FORM_ID}_${START_TIMESPAM}_${TIMESTAMP_NOW}.json"
echo $FILE_PATH

#1.Download main database
curl -u "${USERNAME}:${PASSWORD}" -o ${FILE_PATH} ${URL}

#2.Transform to .csv
python3 file_parser.py ${FILE_PATH} ${DIR_PATH}

#3.Download attachments
python3 surveycto_data_downloader.py ${FILE_PATH} './media' ${USERNAME} ${PASSWORD}
