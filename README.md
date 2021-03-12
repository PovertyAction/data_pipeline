# Setting up VM:

1. Launch AWS Lightsail VM
2. Install boxcryptor
3. Install box
4. Install python
5. Install git
6. Clone this repo
7. Install dependencies (requirements.txt)

# Running pipeline:

'''
python data_processing_pipeline.py '1615378426' 'bdmaskrct' 'maskrct_phone_followup' $env:SURVEYCTO_USERNAME $env:SURVEYCTO_PASSWORD 'X:\\Box Sync\\MASK Test folder' 'X:\\Box Sync\\MASK Test folder\\media
'''

to:

1. Download survey data in json format

```
curl -u "username:password" -o ~/mask_data.json https://bdmaskrct.surveycto.com/api/v2/forms/data/wide/json/maskrct_phone_followup?date=0
```

2. Transform data to .csv
3. Download attachments
