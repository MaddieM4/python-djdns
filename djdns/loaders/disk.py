import json

def DiskLoader(location):
    '''
    Load JSON data from disk.
    '''
    return json.load(open(location))
