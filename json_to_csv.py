import ijson


def parse_json_2(json_filename):

    with open(json_filename, 'rb') as input_file:
        objects = ijson.items(input_file)
        print(objects)

def parse_json(json_filename):
    with open(json_filename, 'rb') as input_file:
        # load json iteratively
        parser = ijson.parse(input_file)
        valid_keys = ['CompletionDate', 'SubmissionDate']
        counter=0
        row = {}
        for prefix, event, value in parser:
            #Check if prefix we are reading is related to one of the expected keys
            if len(prefix.split('.'))>1 and prefix.split('.')[1] in valid_keys:
                key = prefix.split('.')[1]
                #Check if we are starting a new row
                if key == 'CompletionDate':
                    #If row has content, save it to csv
                    if row != {}:
                        print(row)#Save row to csv
                    
                    #Clear row
                    row = {}

                #Add key value to row
                row[key]=value

                counter +=1
             
            #if counter >1000:
            #    break

if __name__ == '__main__':
    parse_json('mask_data_wide_complete.json')
