from nepho import scenario
#from nepho.aws import clidriver

# Valid actions are:
# - create - create a stack
# - delete - delete and clean up a stack
# - show   - print the full pattern configuration and parameters
def call_provider(provider, action, name):
	s = scenario.find_scenario(name)

	if provider == None:
		provider = s['default_provider']
	elif provider not in s['providers']:
		print "Invalid provider for scenario %s, valid providers are: %s" % (name, ', '.join(s['providers']))
		return

	print "Call provider with: %s %s %s" % (provider, action, name)

	#nepho.aws.clidriver.main(stuff)