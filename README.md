1. Download data incrementally

curl -u "username:password" -o ./output_file.json https://bdmaskrct.surveycto.com/api/v2/forms/data/wide/json/maskrct_phone_followup?date=date_timespam

2. Transform data to .csv

python json_to_csv.py data_file.json

3. Download attachments and upload them to box
