# coding: utf-8
import yaml
from nepho.core import base
from os import path
from termcolor import colored

def list(self):
	all_cloudlets = base.all_cloudlets(self)
	dir = ""
	for cloudlet in sorted(all_cloudlets):
		# Print directory if it changes
		if dir != path.dirname(cloudlet):
			dir = path.dirname(cloudlet)
			print dir
		name = path.basename(cloudlet)

		try:
			y = yaml.load(open(path.join(cloudlet, 'cloudlet.yaml')))
		except IOError as e:
			print colored("└──", "yellow"), name, "(", colored("invalid", "red"), ") - missing or malformed cloudlet.yaml!"
		else:
			print colored("└──", "yellow"), name, "(", colored("v%s", "blue") % (y['version']), ")"
