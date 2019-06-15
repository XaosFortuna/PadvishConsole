import ClientManager
import Logger
import Configurations
import time
import os, shutil
import glob
import re



if __name__ == '__main__':
	os.system('reset')


	Logger.Logger('-'*50)

#REVERT TEST CLIENTS TO PROPER SNAPSHOT
	for vm in Configurations.VmNameList:
		ClientManager.Revert(vm, Configurations.VmSnapshot)

#POWER ON TEST CLIENTS
	for vm in Configurations.VmNameList:
		ClientManager.StartVM(vm)
	time.sleep(Configurations.OsStartupTimeout)

#COPY REQUIRED FILES TO CLIENTS
	for vm in Configurations.VmNameList:
		ClientManager.CreateDirectoryOnGuest(vm, Configurations.ClientPath)
		for cfile in Configurations.ClientFilesPath:
			ClientManager.CopyFromHostToGuest(vm, cfile, Configurations.ClientPath + cfile.split('/')[-1:][0])

#COLLECT IPs FROM CLIENTS AND GET THEM TO PADVISH SERVER
	if os.path.isdir(Configurations.CurrentWorkingDirectory[:-1] + '/ClientIPs'):
		shutil.rmtree(Configurations.CurrentWorkingDirectory[:-1] + '/ClientIPs/')
		os.makedirs(Configurations.CurrentWorkingDirectory[:-1] + '/ClientIPs/')
	else:
		os.makedirs(Configurations.CurrentWorkingDirectory[:-1] + '/ClientIPs/')
	if (os.path.isfile(Configurations.CurrentWorkingDirectory[:-1] + '/ClientIPList.txt')):
		os.remove(Configurations.CurrentWorkingDirectory[:-1] + '/ClientIPList.txt')
	for vm in Configurations.VmNameList:
		ClientManager.RunProgramInGuest(vm, Configurations.ClientPath + 'GetIP.exe')
	for vm in Configurations.VmNameList:
		timeout = 0
		while not ClientManager.FileExistsInGuest(vm, 'C:\\ClientIP.txt'):
			time.sleep(1)
			timeout += 1
			print 'file not found'
			if timeout >=10:
				Logger.Logger('cannot find Client ip file in \'%s\''%(vm))
				break
		ClientManager.RenameFileInGuest(vm, 'C:\\ClientIP.txt', 'C:\\%s.txt'%(vm.translate(None, '[]/. -')))
		ClientManager.CopyFromGuestToHost(vm, 'C:\\%s.txt'%(vm.translate(None, '[]/. -')), Configurations.CurrentWorkingDirectory[:-1] + '/ClientIPs/%s.txt'%(vm.translate(None, '[]/. -')))

	for fileName in glob.glob(os.path.join(Configurations.CurrentWorkingDirectory[:-1] + '/ClientIPs', '*.txt')):
		with open(fileName, 'r') as fn:
			with open(Configurations.CurrentWorkingDirectory[:-1] + '/ClientIPList.txt', 'a') as cip:
				cip.write(fn.readline() + '\n') 
				cip.close()
			fn.close()

# PUSH INSTALL DESIRED PRODUCT TO CLIENTS
	Logger.Logger('create push install task and run immediately')
	ClientManager.Revert(Configurations.AmnPardazServerVMName, Configurations.AmnPardazServerSnapshot)
	ClientManager.StartVM(Configurations.AmnPardazServerVMName)
	time.sleep(Configurations.OsStartupTimeout)
	ClientManager.CreateDirectoryOnGuest(Configurations.AmnPardazServerVMName, Configurations.AmnpardazServerPath)
	for d in Configurations.AmnPardazServerDirectories:
		ClientManager.CreateDirectoryOnGuest(Configurations.AmnPardazServerVMName, Configurations.ClientPath + d)
	for sfile in Configurations.AmnPardazServerFiles:
		ClientManager.CopyFromHostToGuest(Configurations.AmnPardazServerVMName, os.path.join(Configurations.CurrentWorkingDirectory[:-1],sfile), (Configurations.AmnpardazServerPath + sfile).replace('/', '\\'))
	ClientManager.RunPythonFile(Configurations.AmnPardazServerVMName, Configurations.AmnpardazServerPath + 'PadvishServerMain.py')

#CHECK CLIENT FOR ANY CRACH OR BSOD

#RESTRAT CLIENTS

##CHECK CLIENT FOR ANY CRACH OR BSOD

#PUSH UNINSTALL





