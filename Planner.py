import Ckpt
import imp, sys

try: from . import Utilities, Fgfs							# being run from parent directory
except SystemError: import Utilities, Fgfs		# being run from ClassCode


class Planner:

	def __init__(sf,wayPts=None):
		sf.wayPts = wayPts
		sf.curPts = sf.wayPts.pop()
		sf.prevDist = 0.0
		sf.prevTime = 0.0
		sf.prevLocation = [0.0,0.0]

	def plan(sf,fDat,fCmd):
	
		if(sf.prevTime == fDat.time): #if the same package, skip
			return
		else:
			curLocation = [fDat.latitude, fDat.longitude]
			print('curLocation', curLocation)
			dist = Utilities.dist(curLocation, sf.prevLocation)
			speed = dist/(fDat.time-sf.prevTime)
			print('speed: ', speed)

			# update variables
			sf.prevTime = fDat.time
			sf.prevLocation = curLocation

