import os

# PATHES
CurrentWorkingDirectory = os.path.dirname(os.path.realpath(__file__)) + '\\'
SqliteWorkingDirectory = CurrentWorkingDirectory + 'Sqlite\\'
TaskCreatorPath = CurrentWorkingDirectory + 'CreateSingleTask.exe'

if os.path.isdir(r'C:\Program Files (x86)\AmnPardaz\Server'):
    ServerPath = 'C:\\Program Files (x86)\\AmnPardaz\\Server\\'
else:
    ServerPath = 'C:\\Program Files\\AmnPardaz\\Server\\'

# SERVICES AND PROCESSES NAMES
AmnPardazServerServiceName = 'AmnPardazServerWinService'

# DATABASE STUFFS
MainDatabaseTasksJobsRetultDict = \
    {'0'      : 'OK', '1000000': 'Start', '1000001': 'Invalid Password', '1000002': 'Login Failed',
     '1000003': 'Unsupported', '1000004': 'Access Denied', '1000005': 'Crash', '1000006': 'Execute',
     '1000007': 'Timeout', '1000008': 'File Copy Fail', '1000009': 'Cannot Restore', '1000010': 'File Not Exists',
     '1000011': 'File Is Corrupted', '1000012': 'Path Not Exists', '1000013': 'Failed',
     '1000014': 'Certificate Error', '1000015': 'Install File Not Found', '1000016': 'Install Error',
     '1000017': 'Client Disconnected',
     '1000018': 'Not Licensed', '1000019': 'Terminated', '1000020': 'Aborted'}

MainDatabaseTasksJobsStatusDict = \
    {0: 'Not Started', 1: 'Finished', 2: 'Fail', 3: 'In Process', 4: 'Prepare'}

MainDatabaseTaskTypes = \
    {
        0 : 'Push Install', 1: 'Virus Scan', 2: 'Restore Quarantine', 3: 'Audit', 4: 'Upgrade',
        7 : 'Force Apply Settings', 8: 'Force Update Now',
        9 : 'Send Message To Client', 10: 'Send Power Command To Client', 11: 'Push Uninstall', 12: 'Change License',
        15: 'Temporary Disable Protection'}
