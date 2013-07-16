import json

def serialize(plugin,opts):
    payload = dict()
    payload['plugin'] = plugin
    payload['opts'] = opts
    return json.dumps(payload, sort_keys=True, indent=2,)
