import os, os.path
import Configurations
import ServiceActions
from shutil import copyfile




def CloneFile(FileName):
	try:
		if os.path.isfile(Configurations.CurrentWorkingDirectory + FileName):
			os.remove(Configurations.CurrentWorkingDirectory + FileName)
		if os.path.isfile(Configurations.CurrentWorkingDirectory + r'Decrypted_' + FileName):
			os.remove(Configurations.CurrentWorkingDirectory + r'Decrypted_' + FileName)

		# ServiceActions.ChangeServiceFailureAction(Configurations.AmnPardazServerServiceName)
		# ServiceActions.StopService(Configurations.AmnPardazServerServiceName)

		copyfile(Configurations.ServerPath + FileName, Configurations.CurrentWorkingDirectory + FileName)

		# ServiceActions.StartService(Configurations.AmnPardazServerServiceName)

	except Exception as e:
		print e.message