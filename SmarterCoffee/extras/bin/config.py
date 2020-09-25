import yaml
import os

class YamlConfig(object):

	def __init__(self, configfile):
		self.configfile = configfile
		self.__cfg = None


	def __open(self):
		try:
			with open(self.configfile, "r") as inp:
				self.__cfg = yaml.load(inp)
		        return 0
		except IOError:               
			return 1
		except yaml.YAMLError,e:
			print "YAML error" + str(e)
			return 2

		# get config value as path to it
	def get(self, path, default=None):
		
		if not self.__cfg:
			if self.__open() != 0:
				assert(False)
			
		components = path.split('/')
		r = self.__cfg
			
		for c in components:			
				if c in r.keys():											
					r = r[c]
				else:
					return default
		return r

