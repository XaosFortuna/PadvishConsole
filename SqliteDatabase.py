import os
import Configurations

os.chdir(Configurations.SqliteWorkingDirectory)


def GetTableNames(DatabaseName):
    TableNamesList = []
    with open(Configurations.SqliteWorkingDirectory + 'TableNamesQuery.txt', 'w') as QueryFile:
        QueryFile.write('.output %s_TableNames.txt \n ' % (DatabaseName[:-3]))
        QueryFile.write('select name from sqlite_master where type = \'table\';\n')
        QueryFile.write('.output stdout')
    os.system('SqliteEnc.exe -enc \"' + Configurations.ServerPath + '%s\" < ' % (
        DatabaseName) + Configurations.SqliteWorkingDirectory + 'TableNamesQuery.txt')
    with open(Configurations.SqliteWorkingDirectory + DatabaseName[:-3] + '_TableNames.txt', 'r') as TableNames:
        for line in TableNames.readlines():
            TableNamesList.append(line[:-2])
    os.remove(Configurations.SqliteWorkingDirectory + DatabaseName[:-3] + '_TableNames.txt')
    os.remove(Configurations.SqliteWorkingDirectory + 'TableNamesQuery.txt')
    return TableNamesList

def GetColumnProperties(DatabaseName, TableName):
    ColumnNamesList = []
    with open(Configurations.SqliteWorkingDirectory + 'ColumnPropertiesQuery.txt', 'w') as QueryFile:
        QueryFile.write('.output %s' % DatabaseName[:-3] + '_%s.txt\n' % (TableName))
        QueryFile.write('PRAGMA TABLE_INFO(%s);\n' % TableName)
        QueryFile.write('.output stdout\n')
    os.system('SqliteEnc.exe -enc \"' + Configurations.ServerPath + '%s\" < ' % (
        DatabaseName) + Configurations.SqliteWorkingDirectory + 'ColumnPropertiesQuery.txt')
    with open(Configurations.SqliteWorkingDirectory + DatabaseName[:-3] + '_%s.txt' % (TableName), 'r') as ColumnName:
        for line in ColumnName.readlines():
            ColumnNamesList.append(line[:-2])
    os.remove(Configurations.SqliteWorkingDirectory + DatabaseName[:-3] + '_%s.txt' % (TableName))
    os.remove(Configurations.SqliteWorkingDirectory + 'ColumnPropertiesQuery.txt')
    return ColumnNamesList

def GetLastNRows(DatabaseName, TableName, ColumnName, OrderBy, n):
    Rows = []
    with open(Configurations.SqliteWorkingDirectory + 'LastNRows.txt', 'w') as QueryFile:
        QueryFile.write('.mode csv\n.output %s' % DatabaseName[:-3] + '_%s_%s.csv\n' % (TableName, n))
        QueryFile.write('select %s from %s order by %s DESC limit %s;\n' % (ColumnName, TableName, OrderBy, n))
        QueryFile.write('.output stdout\n')
    os.system('SqliteEnc.exe -enc \"' + Configurations.ServerPath + '%s\" < ' % (
        DatabaseName) + Configurations.SqliteWorkingDirectory + 'LastNRows.txt')
    with open(Configurations.SqliteWorkingDirectory + DatabaseName[:-3] + '_%s_%s.csv' % (TableName, n), 'r') as Latests:
        for line in Latests.readlines():
            Rows.append(line)
    os.remove(Configurations.SqliteWorkingDirectory + DatabaseName[:-3] + '_%s_%s.csv' % (TableName, n))
    os.remove(Configurations.SqliteWorkingDirectory + 'LastNRows.txt')
    return Rows

def GetSpecificRecord(DatabaseName, TableName, ColumnName, delimiter, delimiterValue):
    Record = []
    with open(Configurations.SqliteWorkingDirectory + 'SpecificRecord.txt', 'w') as QueryFile:
        QueryFile.write('.output %s\n' % (DatabaseName[:-3] + '_%s_%s.txt' % (TableName, ColumnName)))
        QueryFile.write('select %s from %s where %s = %s;\n' % (ColumnName, TableName, delimiter, delimiterValue))
        QueryFile.write('.output stdout\n')
    os.system('SqliteEnc.exe -enc \"' + Configurations.ServerPath + '%s\" < ' % (
        DatabaseName) + Configurations.SqliteWorkingDirectory + 'SpecificRecord.txt')
    with open(Configurations.SqliteWorkingDirectory + DatabaseName[:-3] + '_%s_%s.txt' % (TableName, ColumnName), 'r') as SpecificRecord:
        for line in SpecificRecord.readlines():
            Record.append(line)
    os.remove(Configurations.SqliteWorkingDirectory + DatabaseName[:-3] + '_%s_%s.txt' % (TableName, ColumnName))
    os.remove(Configurations.SqliteWorkingDirectory + 'SpecificRecord.txt')
    return Record
