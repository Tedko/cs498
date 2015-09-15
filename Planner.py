import Ckpt
import imp, sys
import math
import PID

try: from . import Utilities, Fgfs							# being run from parent directory
except SystemError: import Utilities, Fgfs		# being run from ClassCode


class Planner:

	def __init__(sf,wayPts=None):
		sf.wayPts = wayPts
		sf.curPts = sf.wayPts.pop()
		sf.prevDist = 0.0
		sf.prevTime = 0.0
		sf.prevLocation = [0.0,0.0]
		sf.speedPID = PID.PID( -2,2,2 )
		sf.headPID = PID.PID(-0.001,2,2)
		sf.destSpeed = 3.0;
		sf.radius = 2.0

	def plan(sf,fDat,fCmd):


		if(sf.prevTime == fDat.time): #if the same package, skip
			return True
		else:
			timeDiff = fDat.time-sf.prevTime
			curLocation = [fDat.latitude, fDat.longitude]
			print('curLocation', curLocation)
			print('destLocation', sf.curPts[0:2])
			dist = Pdist(curLocation, sf.prevLocation)
			distToWpt = Pdist(curLocation, sf.curPts[0:2])
			print('dist util:', dist)
			print('dist to waypoint', distToWpt)
			speed = dist/(timeDiff)
			print('speed: ', speed)

			curHeading = fDat.head
			destHeading = Pheading(curLocation, sf.curPts[0:2])
			print('heading: ', curHeading)
			print('destheading:', destHeading)

			print('timeDiff: ', timeDiff)
			print('speedPID return: ', sf.speedPID.pid(sf.destSpeed-speed,timeDiff))
			print('headPID return: ', sf.headPID.pid(destHeading-curHeading,timeDiff))

			fCmd.throttle = sf.speedPID.pid(sf.destSpeed-speed,timeDiff)
			fCmd.rudder = (sf.headPID.pid(destHeading-curHeading,timeDiff)/180) - 1

			print('new throttle: ', fCmd.throttle)
			print('new rudder: ', fCmd.rudder)
			print('===================================================')

			# update variables
			sf.prevTime = fDat.time
			sf.prevLocation = curLocation

			i=0
			if(distToWpt < sf.radius):
				i+=1
				print('+++++++++++')
				print(i,'pts is cleared')
				sf.speedPID.pidClear()
				sf.headPID.pidClear()
				if not sf.nextWayPt():
					return False

			return True


	def nextWayPt(sf):
		if not sf.wayPts:
			return False
		else:
			sf.curPts = sf.wayPts.pop()
			return True


# distance function based on http://www.movable-type.co.uk/scripts/latlong.html
# distance in meters
def Pdist(lli,llf):
	R = 6371000.0 #earth's radius
	theta1 = math.radians(lli[0])
	theta2 = math.radians(llf[0])
	dtheta = math.radians(llf[0] - lli[0])
	dlambda = math.radians(llf[1] - lli[1])

	a = math.sin(dtheta/2.0) * math.sin(dtheta/2.0) + math.cos(theta1) * math.cos(theta2) * math.sin(dlambda/2.0) * math.sin(dlambda/2.0)
	c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1-a))
	d = R * c

	return d

# heading function based on http://www.movable-type.co.uk/scripts/latlong.html
# heading in degrees, north being 0
def Pheading(lli, llf):
	theta1 = math.radians(lli[0])
	theta2 = math.radians(llf[0])
	lambda1 = math.radians(lli[1])
	lambda2 = math.radians(llf[1])
	dtheta = math.radians(llf[0] - lli[0])
	dlambda = math.radians(llf[1] - lli[1])

	y = math.sin(lambda2 - lambda1) * math.cos(theta2)
	x = math.cos(theta1) * math.sin(theta2) - math.sin(theta1) * math.cos(theta2) * math.cos(lambda2 - lambda1)

	heading = math.degrees(math.atan2(y, x))%360.0

	return heading
