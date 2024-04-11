import sys, json, argparse

sys.stdout.reconfigure(encoding='utf-8')

testing = 0
#######################
#### CLI ARGUMENTS ####
ap = argparse.ArgumentParser()

ap.add_argument('-fi',
                '--file_in',
                type=str,
                required=True,
                help='path to file to merge from')
ap.add_argument('-ft',
                '--file_to',
                type=str,
                required=True,
                help='path to file to merge to')
ap.add_argument('-fo',
                '--file_out',
                type=str,
                required=True,
                help='path to file to output')

args = vars(ap.parse_args())
if not testing:
    FILE_FROM = args['file_in']
    FILE_TO   = args['file_to']
else:
    FILE_FROM = 'fr0m.json'
    FILE_TO   = 't0.json'
FILE_OUT = 'file_out'
#######################
#### CLI ARGUMENTS ####

if not testing:
    FILE_FROM = 'WSP_efit_info.json'
    FILE_TO   = 'WSP_ppso_info.json'
else:
    FILE_FROM = 'fr0m.json'
    FILE_TO   = 't0.json'
FILE_OUT = 'WSP_info.json'

def is_scalar(var_in) -> bool:
    """Checks if value is scalar or not
    
    Args:
        var_in (any): Value in
    
    Returns:
        bool: true/false
    """ 
    return isinstance(var_in, (str, bool, int, float))

def walk(json_data, path) -> str:
    """Yields nested python object
    
    Args:
        json_data (object): Object to be analyzed
        path (object path): Path to object value
    
    Yields:
        str: path + value
    """
    if(isinstance(json_data, (str, bool, int, float))):
        yield f'{path}: {json_data}'
    if(isinstance(json_data, dict)):
        for key, value in json_data.items():
            yield from walk(value, f'{path}/{key}')
    if(isinstance(json_data, list)):
        for i, value in enumerate(json_data):
            yield from walk(value, f'{path}/[{i}]')

def merge_dicts(json_from, json_to):
    """Marges two dictioneries - from left to right
    
    Args:
        json_from (dict): to merge from
        json_to (dict): to merge to
    
    Raises:
        ValueError: raises error in case 
                    target is not dict or
                    list
    """
    for key, value in json_from.items():
        # Is scalar?
        if is_scalar(value):
            if key in json_to.keys():
                json_to[key] = value
            else:
                json_to[key] = value
        else:
            # Does key exist?
            if key not in json_to.keys():
                if isinstance(value, dict):
                    json_to[key] = {}
                elif isinstance(value, list):
                    json_to[key] = []
                else:
                    raise ValueError('err')
            walk_n_merge(value, json_to[key])

def merge_lists(json_from, json_to):
    """Merges two list
    
    Args:
        json_from (list): to merge from
        json_to (list): to merge to
    """
    for value in json_from:
        # Is scalar?
        if is_scalar(value):
            if value not in json_to:
                json_to.append(value)


def walk_n_merge(json_from, json_to):
    """Merges two Python objects
    
    Args:
        json_from (object): merge from
        json_to (object): merge to
    
    Raises:
        ValueError: if merge from or merge
                    to is not and object,
                    raise error
    """
    # Is source & target dict
    if isinstance(json_from, dict) and isinstance(json_to, dict):
        merge_dicts(json_from, json_to)

    if isinstance(json_from, list) and isinstance(json_to, list):
        merge_lists(json_from, json_to)

    if is_scalar(json_from) and is_scalar(json_to):
        raise ValueError('err!')

    if type(json_from) != type(json_to):
        raise ValueError('err!')

if __name__ == "__main__":
    print('running merge...')

    with open(FILE_FROM, 'r', encoding='utf-8') as fl:
        var = json.load(fl)

    with open(FILE_TO, 'r', encoding='utf-8') as fl:
        var2 = json.load(fl)
    
    walk_n_merge(var, var2)
    out = json.dumps(var2, indent=4)
    
    with open(FILE_OUT, 'w', encoding='utf-8') as fl:
        fl.write(out)

    print('done!')