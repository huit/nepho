from nepho import scenario

def call_provider(provider, action, name):
	s = scenario.find_scenario(name)

	if provider == None:
		provider = s['default_provider']
	elif provider not in s['providers']:
		print "Invalid provider for scenario %s, valid providers are: %s" % (name, ', '.join(s['providers']))
		return

	print "Call provider with: %s %s %s" % (provider, action, name)

#plugin
#import json

#def serialize(subcmd,deployment,opts):
#    payload = dict()
#    payload['subcmd'] = subcmd
#    payload['deployment'] = deployment    
#    payload['opts'] = opts
#    return json.dumps(payload, sort_keys=True, indent=2,)