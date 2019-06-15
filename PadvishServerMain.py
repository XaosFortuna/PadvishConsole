import os, os.path
import SqliteDatabase
import Configurations
# import ServiceActions
# import CloneFile
import RunExecutables
import time
import Logger


if __name__ == '__main__':
    os.chdir(Configurations.CurrentWorkingDirectory)
    # GET TASK ID BEFORE CREATE NEW TASK
    FormerTaskID = int(SqliteDatabase.GetSpecificRecord('main.db', 'tasks_jobs', 'taskid', 'jobid',
                                                        '(SELECT MAX(jobid)  FROM tasks_jobs)')[0])
    print FormerTaskID
    Logger.Logger('create push install task')
    RunExecutables.CreatePushInstallTask()
    while not os.path.isfile('TaskCreates'):
        time.sleep(1)
    os.remove('TaskCreates')

    # GET LATEST TASK ID AND CHECK IF TASK DONE CORRECTLY
    TaskID = int(SqliteDatabase.GetSpecificRecord('main.db', 'tasks_jobs', 'taskid', 'jobid',
                                                  '(SELECT MAX(jobid)  FROM tasks_jobs)')[0])
    while TaskID == FormerTaskID:
        time.sleep(1)
        TaskID = int(SqliteDatabase.GetSpecificRecord('main.db', 'tasks_jobs', 'taskid', 'jobid',
                                                      '(SELECT MAX(jobid)  FROM tasks_jobs)')[0])
    TaskSpecification = SqliteDatabase.GetSpecificRecord('main.db', 'tasks_jobs', '*', 'taskid', TaskID)
    PushCount = len(TaskSpecification)
    for row in TaskSpecification:
        JobId = int(row.split(',')[0])
        Status = int(row.split(',')[4])
        TargetIp = str(row.split(',')[3])
        TaskResult = row.split(',')[5]
        print 'push install task for (%s) is in process\nplease wait ...'%(TargetIp).title()
        while Status == 0 or Status == 3 or Status == 4:
            time.sleep(1)
            r = SqliteDatabase.GetSpecificRecord('main.db', 'tasks_jobs', '*', 'jobid', JobId)
            Status = int(r[0].split(',')[4])
            TargetIp = str(r[0].split(',')[3])
            TaskResult = r[0].split(',')[5]
        if Status == 1:
            Logger.Logger('push install done for (%s)'%(TargetIp).title())
        else:
            Logger.Logger(
                    'task status \"'.title() + Configurations.MainDatabaseTasksJobsStatusDict.get(
                        Status) + '\" For (' + TargetIp + ') Reason: ' +
                    Configurations.MainDatabaseTasksJobsRetultDict.get(str(TaskResult)))

    # for i in SqliteDatabase.GetTableNames('main.db'):
    #     print i

    # for i in SqliteDatabase.GetColumnProperties('main.db', 'tasks_jobs'):
    #     print i

    # print SqliteDatabase.GetLastNRows('main.db', 'tasks_jobs', '*', 'jobid', 100)
