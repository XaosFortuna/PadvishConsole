import os, os.path
import SqliteDatabase
import Configurations
import ServiceActions
import CloneFile
import threading
import RunExecutables
import time



if __name__ == '__main__':
	def TaskStatus():
		while not os.path.isfile(Configurations.CurrentWorkingDirectory + 'TaskCreates'):
			time.sleep(1000)
			print 'wait'
		os.remove(Configurations.CurrentWorkingDirectory + 'TaskCreates')
		#GET LATEST TASK ID AND CHECH IF TASK DONE CORRECTLY
		CloneFile.CloneFile('main.db')
		SqliteDatabase.DataBaseDecrypter('main.db')
		LatestTaskID = SqliteDatabase.GetLastValue('Decrypted_main.db', 'tasks_jobs', 'taskid')
		for i in SqliteDatabase.GetSpecificValue('Decrypted_main.db', 'tasks_jobs', '*', 'taskid', LatestTaskID + 1):
			while i[4] == 3:
				time.sleep(1000)
			if i[4] == 1:
				print 'task is already finished!'.title()
			else:
				print 'task status : \"'.title() + Configurations.MainDatabaseTasksJobsStatusDict.get(i[4]) + '\" For ' + i[3] + ' Reason : ' + Configurations.MainDatabaseTasksJobsRetultDict.get(str(i[5]))


	#CREATE TASK AND WAIT FOR CREATION
	threading.Thread(target = RunExecutables.CreatePushInstallTask).start()
	threading.Thread(target = TaskStatus).start()


	#RUN TASK
	# os.system(Configurations.TaskCreatorPath)
	# 
	# 




	# TableNamesList = ConsoleDataBase.DataBaseTableNames('Decrypted_main.db')
	# for t in TableNamesList:
	# 	print '----------\n' +  t + '\n----------'
	# 	ColumnsProperties = ConsoleDataBase.ColumnsProperties('Decrypted_main.db', t)
	# 	for i in ColumnsProperties:
	# 		print i, ColumnsProperties[i]
	# for i in ConsoleDataBase.DataBaseTableNames('Decrypted_main.db'):
	# 	print i
	
	# c = SqliteDatabase.ColumnsProperties('Decrypted_main.db', 'tasks_jobs')
	# for i in c:
	# 	print i, c[i]
	

	
	# print SqliteDatabase.ReadLastNRow('Decrypted_main.db', 'tasks_jobs', '*', 'jobid', 100)