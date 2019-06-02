import os


def ChangeServiceFailureAction(ServiceName):
	try:
		os.system('sc failure %s reset= 86400 actions= //////'%(ServiceName))
	except Exception as e:
		print e.message

def StopService(ServiceName):
	try:
		os.system('sc config %s start= disabled'%(ServiceName))
		os.system('sc stop %s'%(ServiceName))
	except Exception as e:
		print e.message


def StartService(ServiceName):
	try:
		os.system(r'sc config %s start= delayed-auto'%(ServiceName))
		os.system(r'sc start %s'%(ServiceName))
	except Exception as e:
		raise e

