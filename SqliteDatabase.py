import os
import operator
import sqlite3
import Configurations





def DataBaseDecrypter(DBName):
	#This Method Decrypts Encrypted Input Sqlite Database File
	Input = open (Configurations.CurrentWorkingDirectory + DBName, 'rb')
	Output = open (Configurations.CurrentWorkingDirectory + 'Decrypted_' + DBName, 'ab')
	Counter = 0
	print 'Decrypter is running. please wait ...'.title()
	while 1:
		try:
			byte = Input.read(1)
			if not byte:
				break
			Wrapper = ((1+Counter)*(1+Counter)*1997)%991
			Ucode = ord(byte)
			newbyte = operator.xor(Ucode,Wrapper)
			newbyte = operator.__and__(newbyte,255)
			Output.write(chr(newbyte))
			Counter += 1
		except Exception as e:
			print e.message
	Input.close()
	Output.close()


def DataBaseTableNames(DBName):
	#This Method Returns All Table Names Of Given Database
	TablesNameList = []
	Input = Configurations.CurrentWorkingDirectory + DBName
	try:
		Conn = sqlite3.connect(Input)
		Cursor = Conn.cursor()
		for row in Cursor.execute('select name from sqlite_master where type = \'table\''):
			TablesNameList.append(row[0])
		return TablesNameList
	except Exception as e : 
		print e.message


def ColumnsProperties(DbName, TableName):
	#This Method Returns A Dictionary Of Columns Name And Column Type Of Given Table
	Columns = {}
	DataBasePath = Configurations.CurrentWorkingDirectory + DbName
	try:
		Conn = sqlite3.connect(DataBasePath)	
		Cursor = Conn.cursor()
		for row in  Cursor.execute('PRAGMA TABLE_INFO(%s)'%TableName):
			Columns[row[1]] = row[2] 
		return Columns
	except Exception as e:
		print e.message


def ReadLastNRow(DbName, TableName, ColumnName, OrderBy ,n):
	DataBasePath = Configurations.CurrentWorkingDirectory + DbName
	try:
		Conn = sqlite3.connect(DataBasePath)	
		Cursor = Conn.cursor()
		for row in  Cursor.execute('select %s from %s order by %s DESC limit %s'%(ColumnName ,TableName, OrderBy, n)): #DESC
			return row
	except Exception as e:
		print e.message


def GetLastValue(DbName, TableName, ColumnName):
	DataBasePath = Configurations.CurrentWorkingDirectory + DbName
	try:
		Conn = sqlite3.connect(DataBasePath)	
		Cursor = Conn.cursor()
		for row in  Cursor.execute('select %s from %s order by %s DESC limit 1'%(ColumnName, TableName, ColumnName)): #DESC
			return row[0]
	except Exception as e:
		print e.message


def GetSpecificValue(DbName, TableName, ColumnName, delimiter, delimiterValue):
	#THIS METHOD RETURNS A LIST OF VALUES OF SPECIFIC COLUMN
	DataBasePath = Configurations.CurrentWorkingDirectory + DbName
	ValueList = []
	try:
		Conn = sqlite3.connect(DataBasePath)	
		Cursor = Conn.cursor()
		for row in  Cursor.execute('select %s from %s where %s = %s'%(ColumnName, TableName, delimiter, delimiterValue)): #DESC
			ValueList.append(row)
		return ValueList
	except Exception as e:
		print e.message




