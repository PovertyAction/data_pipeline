import ijson
import pandas as pd
csv_file = "X:\Box\Mask VM all data\Mask_data\maskrct_field_followup.csv"

df = pd.read_csv(csv_file)

print(df.shape)

json_filename = "X:\Box\Mask VM all data\Mask_data\maskrct_field_followup.json"

with open(json_filename, 'rb') as input_file:
    # load json iteratively
    parser = ijson.parse(input_file)

    rows_counter=0

    for prefix, event, value in parser:
        #Check if prefix we are reading is a json key
        if len(prefix.split('.'))>1:
            key = prefix.split('.')[1]

            #First lets check we are not starting a new row. If we are, we should save the previous one and start a new one
            if key == 'CompletionDate':
                print(value)
