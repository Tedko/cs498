# Simple example of taxiing as scripted behavior
# import Pilot; a=Pilot.Pilot(); a.start()

import Ckpt
import imp, sys
import Planner

try: from . import Utilities, Fgfs							# being run from parent directory
except SystemError: import Utilities, Fgfs		# being run from ClassCode

def rel():
	imp.reload(sys.modules['Pilot'])

class Pilot (Ckpt.Ckpt):			# subclass of the class Ckpt in the file Ckpt

	def __init__(sf,tsk='MP2',rc=False,gui=False):
		super().__init__(tsk, rc, gui)
		sf.strtTime = None
		sf.duration = None

		tempWayPts = sf.getWayPts(tsk)
		tempWayPts.reverse()
		sf.planner = Planner.Planner(tempWayPts)

	def ai(sf,fDat,fCmd):
		'''Override with the Pilot decision maker, args: fltData and cmdData from Utilities.py'''
		# curLocation = [fDat.latitude, fDat.longitude]
		# print('AI location', curLocation)

		if not sf.planner.plan(fDat, fCmd):
			return 'stop'
