import psycopg2
import sys
import configparser

class DatabaseConn:
	def __init__(self, configFile, sections):
		configs = DatabaseConn.generateConfig(configFile, sections)
		self.conn = psycopg2.connect('host='+ configs['host'] + ' port=' + configs['port'] + ' dbname=' + configs['dbname'] + ' user=' + configs['user'])

	def readData(self, command):
		try: 
			cur = self.conn.cursor()
			print('executing command...')
			cur.execute(command)
			result = cur.fetchall()
			cur.close()
			return result
		except:
			print('----------- ERROR --------------------')
			print(sys.exc_info()[1])
			self.conn.rollback()
			print('--------------------------------------')

	def executeCommand(self, command):
		try:
			cur = self.conn.cursor()
			print('executing command...')
			cur.execute(command)
			self.conn.commit()
			print('command executed...')
			cur.close()
		except:
			print('----------- ERROR --------------------')
			print(sys.exc_info()[1])
			self.conn.rollback()
			print('--------------------------------------')

	@staticmethod
	def generateConfig(file, sections):
		Config = configparser.RawConfigParser()
		Config.read(file)
		def ConfigSectionMap(section):
			dict1 = {}
			options = Config.options(section)
			for option in options:
				try:
					dict1[option] = Config.get(section, option)
					if dict1[option] == -1:
						DebugPrint("skip: %s" % option)
				except:
					print("exception on %s!" % option)
					dict1[option] = None
			return dict1
		settings = ConfigSectionMap(sections)
		return settings		

