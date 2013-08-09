import json

def serialize(subcmd,deployment,opts):
    payload = dict()
    payload['subcmd'] = subcmd
    payload['deployment'] = deployment    
    payload['opts'] = opts
    return json.dumps(payload, sort_keys=True, indent=2,)
