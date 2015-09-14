import Ckpt
import imp, sys
import math

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
			print('destLocation', sf.curPts[0:1])
			dist = Utilities.dist(curLocation, sf.prevLocation)
			print('dist util:', dist)
			print('Pdist', Pdist(curLocation, sf.curPts[0:1]))
			speed = dist/(fDat.time-sf.prevTime)
			print('speed: ', speed)

			# update variables
			sf.prevTime = fDat.time
			sf.prevLocation = curLocation

			curHeading = fDat.head
			print('heading: ', curHeading)
			print('destheading:', Pheading(curLocation, sf.curPts[0:1]))

# distance function based on http://www.movable-type.co.uk/scripts/latlong.html
# distance in meters
def Pdist(lli,llf):
	R = 6371000.0
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



