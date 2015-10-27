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

	def __init__(sf,tsk='HW4a',rc=False,gui=False):
		super().__init__(tsk, rc, gui)
		sf.strtTime = None
		sf.duration = None

		sf.planner = Planner.Planner(10,2000,200)#angle(pitch),alchange,finalspeed

	def ai(sf,fDat,fCmd):
		'''Override with the Pilot decision maker, args: fltData and cmdData from Utilities.py'''

		if not sf.planner.plan(fDat, fCmd):
			return 'stop'
