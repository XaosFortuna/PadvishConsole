import os
import operator
import sqlite3
import Configuratoins





def DataBaseDecrypter(DBName):
	#This Method Decrypts Encrypted Input Sqlite Database File
	Input = open (Configuratoins.CurrentWorkingDirectory + DBName, 'rb')
	Output = open (Configuratoins.CurrentWorkingDirectory + 'Decrypted_' + DBName, 'ab')
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
	Input = Configuratoins.CurrentWorkingDirectory + DBName
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
	DataBasePath = Configuratoins.CurrentWorkingDirectory + DbName
	try:
		Conn = sqlite3.connect(DataBasePath)	
		Cursor = Conn.cursor()
		for row in  Cursor.execute('PRAGMA TABLE_INFO(%s)'%TableName):
			Columns[row[1]] = row[2] 
		return Columns
	except Exception as e:
		print e.message


def ReadLastNRow(DbName, TableName, n):
	DataBasePath = Configuratoins.CurrentWorkingDirectory + DbName
	try:
		Conn = sqlite3.connect(DataBasePath)	
		Cursor = Conn.cursor()
		for row in  Cursor.execute('select * from %s order by id DESC limit %s'%(TableName,n)):
			print row
	except Exception as e:
		print e.message

