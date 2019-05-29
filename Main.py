import os, os.path
import ConsoleDataBase
import Configuratoins
from shutil import copyfile


if __name__ == '__main__':
	if os.path.isfile(Configuratoins.CurrentWorkingDirectory + r'main.db'):
		os.remove(Configuratoins.CurrentWorkingDirectory + r'main.db')
	if os.path.isfile(Configuratoins.CurrentWorkingDirectory + r'Decrypted_main.db'):
		os.remove(Configuratoins.CurrentWorkingDirectory + r'Decrypted_main.db')
	copyfile(Configuratoins.ServerPath + r'main.db' , Configuratoins.CurrentWorkingDirectory + r'main.db')
	ConsoleDataBase.DataBaseDecrypter('main.db')
	ConsoleDataBase.ReadLastNRow('Decrypted_main.db', 'tasks', 4)
	# for i in ConsoleDataBase.DataBaseTableNames('Decrypted_main.db'):
	# 	print i
	# c = ConsoleDataBase.ColumnsProperties('Decrypted_main.db', 'tasks')
	# print c 
