import ijson
import sys

def get_json_keys(json_filename):

    all_keys = []

    with open(json_filename, 'rb') as input_file:
        # load json iteratively
        parser = ijson.parse(input_file)
        for prefix, event, value in parser:
            #Check if prefix we are reading is a json key
            if len(prefix.split('.'))>1:
                key = prefix.split('.')[1]

                if key not in all_keys:
                    all_keys.append(key)
    return all_keys


if __name__ == '__main__':
    json_file = sys.argv[1]
    json_keys = get_json_keys(json_file)
    print(f'json_keys: {json_keys}')
