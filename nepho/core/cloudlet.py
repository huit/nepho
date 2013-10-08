# coding: utf-8
import yaml
from nepho.core import common
from os import path
from termcolor import colored

def list_all(self):
	all_cloudlets = common.all_cloudlets(self)
	dir = ""
	items = list()
	for cloudlet in sorted(all_cloudlets):
		# Print directory if it changes
		if dir != path.dirname(cloudlet):
			dir = path.dirname(cloudlet)
			print colored(dir, "cyan")
		name = path.basename(cloudlet)

		# If there are multiple versions of a cloudlet with the same name,
		# subsequent versions will be ignored by other commands
		if name not in items:
			try:
				y = yaml.load(open(path.join(cloudlet, 'cloudlet.yaml')))
			except:
				print colored("└──", "yellow"), name, "(", colored("error", "red"), "- missing or malformed cloudlet.yaml )"
			else:
				print colored("└──", "yellow"), name, "(", colored("v%s", "blue") % (y['version']), ")"
			items.append(name)
		else:
			print colored("└──", "yellow"), name, "(", colored("error", "red"), "- duplicate cloudlet will be ignored )"
			
	return