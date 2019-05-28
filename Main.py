import os
import ConsoleDataBase


if __name__ == '__main__':
	
	# ConsoleDataBase.DataBaseDecrypter('main.db')
	# for i in ConsoleDataBase.DataBaseTableNames('Decrypted_main.db'):
	# 	print i
	# c = ConsoleDataBase.ColumnsProperties('Decrypted_main.db', 'tasks')
	# print c 

	ConsoleDataBase.ReadLastNRow('Decrypted_main.db', 'reports', 4)