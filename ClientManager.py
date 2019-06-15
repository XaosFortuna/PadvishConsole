import urllib
import json
import os, os.path
import time
from datetime import datetime, timedelta
from time import gmtime, strftime
import hashlib
import sys
import subprocess
import datetime
import glob
import Logger
import Configurations




def GetVmNameList():
	VmList = []
	try:
		os.system("vmrun -T esx -h %s -u %s -p %s list > %s.txt"%(Configurations.ServerAddress, Configurations.ServerUserName, Configurations.ServerPassword, os.path.join(Configurations.CurrentWorkingDirectory[:-1], 'VmNameList')))
		with open(os.path.join(Configurations.CurrentWorkingDirectory[:-1], 'VmNameList.txt'), 'r') as vmlist:
			next(vmlist)
			for line in vmlist:
				VmList.append(line[:-1])
		os.remove(os.path.join(Configurations.CurrentWorkingDirectory[:-1], 'VmNameList.txt'))
		return VmList
	except Exception as e:
		Logger.Logger(e.message)

def Revert(vm, snapshot):
	Logger.Logger("Reverting %s to %s snapshot. Please wait..."%(vm, snapshot))
	try:
		os.system("vmrun -T esx -h %s -u %s -p %s revertToSnapshot \"%s\" %s" \
			%(Configurations.ServerAddress, Configurations.ServerUserName, Configurations.ServerPassword, vm, snapshot))
	except Exception as e:
		Logger.Logger(e.message)
	
def StartVM(vm):
	Logger.Logger("%s turned on"%(vm))
	try:
		os.system("vmrun -T esx -h %s -u %s -p %s stop  \"%s\" soft"\
		 %(Configurations.ServerAddress, Configurations.ServerUserName, Configurations.ServerPassword, vm))
		time.sleep(5)
		os.system("vmrun -T esx -h %s -u %s -p %s start \"%s\"" \
			%(Configurations.ServerAddress, Configurations.ServerUserName, Configurations.ServerPassword, vm))
	except Exception as e:
		Logger.Logger(e.message)

def StopVM(vm):
	try:
		Logger.Logger("%s stopped"%(vm))
		os.system("vmrun -T esx -h %s -u %s -p %s stop  \"%s\" soft" \
			%(Configurations.ServerAddress, Configurations.ServerUserName, Configurations.ServerPassword, vm))
	except Exception as e:
		Logger.Logger(e.message)

def RestartVM(vm):
	Logger.Logger("%s restarted"%(vm))
	os.system("vmrun -T esx -h %s -u %s -p %s reset  \"%s\" soft" %(Configurations.ServerAddress, Configurations.ServerUserName, Configurations.ServerPassword, vm))

def CopyFromHostToGuest(VM, sourcePath, destinationPath, mode=""):
	try:
		Logger.Logger('copying file form \'%s\' to \'%s\''%(sourcePath, destinationPath))
		os.system("vmrun -T esx -h \'%s\' -u \'%s\' -p \'%s\' -gu \'%s\' -gp \'%s\' copyFileFromHostToGuest \'%s\' \'%s\' \'%s\'" \
			%(Configurations.ServerAddress, Configurations.ServerUserName, Configurations.ServerPassword, Configurations.VmsUserName, Configurations.VmsPassword, VM, sourcePath, destinationPath))
	except Exception as e:
		Logger.Logger(e.message)

def CopyFromGuestToHost(VM, sourcePath, destinationPath):
	try:
		Logger.Logger('copying file form \'%s\' to \'%s\''%(sourcePath, destinationPath))
		os.system("vmrun -T esx -h \'%s\' -u \'%s\' -p \'%s\' -gu \'%s\' -gp \'%s\' copyFileFromGuestToHost \'%s\' \'%s\' \'%s\'" \
			%(Configurations.ServerAddress, Configurations.ServerUserName, Configurations.ServerPassword, Configurations.VmsUserName, Configurations.VmsPassword, VM, sourcePath, destinationPath))
		timeout = 0
		while not os.path.isfile(destinationPath):
			print 'Copying %s is in process'.title()
			timeout += 1
			time.sleep(1)
			if timeout >= 10:
				break
		while not os.path.isfile(destinationPath):
			Logger.Logger('file copying failed! : %s'%(destinationPath))

	except Exception as e:
		Logger.Logger(e.message)

def CreateDirectoryOnGuest(vm, DirPath):
	try:
		Logger.Logger('create %s on %s'%(DirPath, vm))
		os.system("vmrun -T esx -h \'%s\' -u \'%s\' -p \'%s\' -gu %s -gp %s createDirectoryInGuest \'%s\' \'%s\'" \
			%(Configurations.ServerAddress, Configurations.ServerUserName, Configurations.ServerPassword, Configurations.VmsUserName, Configurations.VmsPassword, vm, DirPath))
	except Exception as e:
		Logger.Logger(e.message)

def RunProgramInGuest(VM, exeFile):
	try:
		Logger.Logger('Execute %s on %s'%(exeFile, VM))
		os.system("vmrun -T esx -h \'%s\' -u \'%s\' -p \'%s\' -gu %s -gp %s runProgramInGuest \'%s\' -nowait \'%s\'" \
			%(Configurations.ServerAddress, Configurations.ServerUserName, Configurations.ServerPassword, Configurations.VmsUserName, Configurations.VmsPassword, VM, exeFile))
	except Exception as e:
		Logger.Logger(e.message)

def RenameFileInGuest(VM, oldFilePath, newFilePath):
	try:
		Logger.Logger('Remane file in %s form \'%s\' to \'%s\''%(VM, oldFilePath, newFilePath))
		os.system("vmrun -T esx -h \'%s\' -u \'%s\' -p \'%s\' -gu \'%s\' -gp \'%s\' renameFileInGuest \'%s\' \'%s\' \'%s\'" \
			%(Configurations.ServerAddress, Configurations.ServerUserName, Configurations.ServerPassword, Configurations.VmsUserName, Configurations.VmsPassword, VM, oldFilePath, newFilePath))
	except Exception as e:
		Logger.Logger(e.message)

def FileExistsInGuest(VM, filePath):
	try:
		Logger.Logger('check if file exists in \'%s\''%(VM))
		if(os.system("vmrun -T esx -h \'%s\' -u \'%s\' -p \'%s\' -gu \'%s\' -gp  \'%s\' fileExistsInGuest \'%s\' \'%s\'" \
			%(Configurations.ServerAddress, Configurations.ServerUserName, Configurations.ServerPassword, Configurations.VmsUserName, Configurations.VmsPassword, VM, filePath))==0):	
			return True
		else:
			return False
	except Exception as e:
		Logger.Logger(e.message)

def RunPythonFile(VM, pyFile, arg = ''):
	Logger.Logger('')
	if(arg!=''):
		#-activeWindow -interactive -nowait
		os.system("vmrun -T esx -h \'%s\' -u \'%s\' -p \'%s\' -gu \'%s\' -gp \'%s\' runProgramInGuest \'%s\' -interactive 'c:\\python27\\python.exe' \'%s\' \'%s\'" \
			%(Configurations.ServerAddress, Configurations.ServerUserName, Configurations.ServerPassword, Configurations.VmsUserName, Configurations.VmsPassword, VM, pyFile, arg))
	else:
		os.system("vmrun -T esx -h \'%s\' -u \'%s\' -p \'%s\' -gu \'%s\' -gp \'%s\' runProgramInGuest \'%s\' -interactive 'c:\\python27\\python.exe' \'%s\'" \
			%(Configurations.ServerAddress, Configurations.ServerUserName, Configurations.ServerPassword, Configurations.VmsUserName, Configurations.VmsPassword, VM, pyFile))
