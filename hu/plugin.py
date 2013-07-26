import json

def serialize(subcmd,modul,opts):
    payload = dict()
    payload['subcmd'] = subcmd
    payload['module'] = modul    
    payload['opts'] = opts
    return json.dumps(payload, sort_keys=True, indent=2,)
