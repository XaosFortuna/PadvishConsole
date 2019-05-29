import os


CurrentWorkingDirectory = os.path.dirname(os.path.realpath(__file__)) + '\\'

if os.path.isdir(r'C:\Program Files (x86)\AmnPardaz\Server'):
	ServerPath = r'C:\Program Files (x86)\AmnPardaz\Server\\'
else:
	ServerPath = r'C:\Program Files\AmnPardaz\Server\\'
