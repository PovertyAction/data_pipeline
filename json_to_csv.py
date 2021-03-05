import ijson
import pandas as pd

def parse_json_2(json_filename):

    with open(json_filename, 'rb') as input_file:
        objects = ijson.items(input_file)
        print(objects)

def parse_json(json_filename):

    df = pd.DataFrame()

    with open(json_filename, 'rb') as input_file:
        # load json iteratively
        parser = ijson.parse(input_file)
        #valid_keys = ['CompletionDate', 'SubmissionDate']
        rows_counter=0
        row = {}
        for prefix, event, value in parser:
            #Check if prefix we are reading is related to one of the expected keys
            if len(prefix.split('.'))>1:# and prefix.split('.')[1] in valid_keys:
                key = prefix.split('.')[1]

                #If key is CompletionDate, we are starting a new row, add it to df and clear row dict
                if key == 'CompletionDate':

                    if row != {}:
                        df = df.append(row, ignore_index=True)

                        if rows_counter % 50 == 0:
                            print(df)

                        rows_counter +=1

                    #Clear row
                    row = {}

                #Add key value to row
                row[key]=value





if __name__ == '__main__':
    parse_json('mask_data_wide_complete.json')
