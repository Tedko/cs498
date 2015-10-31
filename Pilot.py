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
		sf.counter = 1
		sf.alchange = 2000
		sf.angle = 10
		sf.finalspeed = 500
		sf.planner = Planner.Planner(sf.angle,sf.alchange,sf.finalspeed)#angle,alchange,finalspeed
	def pc(sf,fDat,fCmd):
		ret = sf.planner.pc(fDat,fCmd)
		if ret=='OK' :
			sf.planner = Planner.Planner(sf.angle,sf.alchange,sf.finalspeed)#nothing
		else :
			sf.planner = Planner.Planner(int(ret[0]),sf.alchange,int(ret[1]) )

	def ai(sf,fDat,fCmd):
		if sf.counter==1 :
			sf.pc(fDat,fCmd)
		sf.counter += 1
		if sf.planner.do(fDat, fCmd) == 'DONE':
			return 'stop'

	def test():
		pass
