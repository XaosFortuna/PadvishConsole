import os
import Configurations

os.chdir(Configurations.SqliteWorkingDirectory)


def GetTableNames(DatabaseName):
    TableNamesList = []
    with open(DatabaseName[:-3] + '_TableNames.txt', 'w'):
        with open('TableNamesQuery.txt', 'w') as QueryFile:
            QueryFile.write('.output %s_TableNames.txt \n ' % (DatabaseName[:-3]))
            QueryFile.write('select name from sqlite_master where type = \'table\';\n')
            QueryFile.write('.output stdout')
        os.system('Sqlite\\SqliteEnc.exe -enc \"' + Configurations.ServerPath + '%s\" < ' % (
            DatabaseName) + Configurations.CurrentWorkingDirectory + 'TableNamesQuery.txt')
    with open(DatabaseName[:-3] + '_TableNames.txt', 'r') as TableNames:
        for line in TableNames.readlines():
            TableNamesList.append(line[:-2])
    os.remove(DatabaseName[:-3] + '_TableNames.txt')
    os.remove('TableNamesQuery.txt')
    return TableNamesList


def GetColumnProperties(DatabaseName, TableName):
    ColumnNamesList = []
    with open(DatabaseName[:-3] + '_%s.txt' % TableName, 'w'):
        with open('ColumnPropertiesQuery.txt', 'w') as QueryFile:
            QueryFile.write('.output %s' % DatabaseName[:-3] + '_%s.txt\n' % TableName)
            QueryFile.write('PRAGMA TABLE_INFO(%s);\n' % TableName)
            QueryFile.write('.output stdout\n')
        os.system('Sqlite\\SqliteEnc.exe -enc \"' + Configurations.ServerPath + '%s\" < ' % (
            DatabaseName) + Configurations.CurrentWorkingDirectory + 'ColumnPropertiesQuery.txt')
    with open(DatabaseName[:-3] + '_%s.txt' % TableName, 'r') as ColumnName:
        for line in ColumnName.readlines():
            ColumnNamesList.append(line[:-2])
    os.remove(DatabaseName[:-3] + '_%s.txt' % TableName)
    os.remove('ColumnPropertiesQuery.txt')
    return ColumnNamesList


def GetLastNRows(DatabaseName, TableName, ColumnName, OrderBy, n):
    Rows = []
    with open(DatabaseName[:-3] + '_%s_%s.csv' % (TableName, n), 'w'):
        with open('LastNRows.txt', 'w') as QueryFile:
            QueryFile.write('.mode csv\n.output %s' % DatabaseName[:-3] + '_%s_%s.csv\n' % (TableName, n))
            QueryFile.write('select %s from %s order by %s DESC limit %s;\n' % (ColumnName, TableName, OrderBy, n))
            QueryFile.write('.output stdout\n')
        os.system('Sqlite\\SqliteEnc.exe -enc \"' + Configurations.ServerPath + '%s\" < ' % (
            DatabaseName) + Configurations.CurrentWorkingDirectory + 'LastNRows.txt')
    with open(DatabaseName[:-3] + '_%s_%s.csv' % (TableName, n), 'r') as Latests:
        for line in Latests.readlines():
            Rows.append(line)
    os.remove(DatabaseName[:-3] + '_%s_%s.csv' % (TableName, n))
    os.remove('LastNRows.txt')
    return Rows


def GetSpecificRecord(DatabaseName, TableName, ColumnName, delimiter, delimiterValue):
    Record = []
    with open(DatabaseName[:-3] + '_%s_.txt' % TableName, 'w'):
        with open('SpecificRecord.txt', 'w') as QueryFile:
            QueryFile.write('.mode csv\n.output %s\n' % (DatabaseName[:-3] + '_%s_.txt' % TableName))
            QueryFile.write('select %s from %s where %s = %s;\n' % (ColumnName, TableName, delimiter, delimiterValue))
            QueryFile.write('.output stdout\n')
            QueryFile.write('.exit\n')
        os.system('Sqlite\\SqliteEnc.exe -enc \"' + Configurations.ServerPath + '%s\" < ' % (
            DatabaseName) + Configurations.CurrentWorkingDirectory + 'SpecificRecord.txt')
    with open(DatabaseName[:-3] + '_%s_.txt' % TableName, 'r') as SpecificRecord:
        for line in SpecificRecord.readlines():
            Record.append(line[:-1])
    os.remove(DatabaseName[:-3] + '_%s_.txt' % TableName)
    os.remove('SpecificRecord.txt')
    return Record
