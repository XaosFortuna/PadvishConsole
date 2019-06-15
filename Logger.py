import os
import datetime



def Logger(message):
	print message
	now = datetime.datetime.now()
	logFileName = '%02d-%02d-%d.txt'%(now.day, now.month, now.year)
	TodayLog = open('Logs/%s'%logFileName, 'a')
	TodayLog.write('%02d:%02d:%02d >\t'%(now.hour, now.minute, now.second))
	TodayLog.write(message.title() + '\n')
	TodayLog.close()






