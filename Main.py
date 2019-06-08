import os, os.path
import SqliteDatabase
import Configurations
import ServiceActions
import CloneFile
import RunExecutables
import time

if __name__ == '__main__':

    # RunExecutables.CreatePushInstallTask()
    # while not os.path.isfile(Configurations.CurrentWorkingDirectory + 'TaskCreates'):
    # 	time.sleep(1000)
    # os.remove(Configurations.CurrentWorkingDirectory + 'TaskCreates')

    # GET LATEST TASK ID AND CHECK IF TASK DONE CORRECTLY
    # CloneFile.CloneFile('main.db')
    # SqliteDatabase.DataBaseDecrypter('main.db')
    LatestTaskID = SqliteDatabase.GetLastRecord('Decrypted_main.db', 'tasks_jobs', 'taskid')
    print LatestTaskID

    for i in SqliteDatabase.GetSpecificRecord('Decrypted_main.db', 'tasks_jobs', '*', 'taskid', LatestTaskID):
        print 'taskid is : ' + str(i)

        while i[4] == 3:
            time.sleep(1000)
        if i[4] == 1:
            print 'task is already finished!'.title()
        else:
            print 'task status : \"'.title() + Configurations.MainDatabaseTasksJobsStatusDict.get(i[4]) + '\" For ' + i[
                3] + ' Reason : ' + Configurations.MainDatabaseTasksJobsRetultDict.get(str(i[5]))

    # TableNamesList = ConsoleDataBase.DataBaseTableNames('Decrypted_main.db')
    # for t in TableNamesList:
    # 	print '----------\n' +  t + '\n----------'
    # 	ColumnsProperties = ConsoleDataBase.ColumnsProperties('Decrypted_main.db', t)
    # 	for i in ColumnsProperties:
    # 		print i, ColumnsProperties[i]
    # for i in SqliteDatabase.DataBaseTableNames('Decrypted_main.db'):
    # 	print i

    # c = SqliteDatabase.ColumnsProperties('Decrypted_main.db', 'tasks')
    # for i in c:
    # 	print i, c[i]

    for i in SqliteDatabase.ReadLastNRow('Decrypted_main.db', 'tasks', 'task_type', 'id', 1):
        print i

# print SqliteDatabase.ReadLastNRow('Decrypted_main.db', 'tasks_jobs', '*', 'jobid', 100)
