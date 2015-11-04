import Ckpt
import imp, sys
import math
import PID

try: from . import Utilities, Fgfs							# being run from parent directory
except SystemError: import Utilities, Fgfs		# being run from ClassCode


class Planner:

	def __init__(sf,angle,alchange,finalspeed):
		sf.firstRun = True
		sf.startTime = 0.0
		sf.prevTime = 0.0
		sf.speedPID = PID.PID( 0.053,0.00008,0.01 )
		sf.rollPID = PID.PID( 0.002,0.001,0.001 )
		sf.pitchPID = PID.PID( -0.009,-0.001,-0.0001 )#pitch 1 goes down
		sf.destSpeed = finalspeed
		sf.destSpeedcp = finalspeed
		sf.roll = 0
		sf.altitude = 2000
		sf.prevAltitude = 2000
		sf.prevLocation = [37.613555908203125, -122.35719299316406]#start pt
		sf.alchange = alchange
		sf.destAngle = angle
		sf.destAnglecp = angle
		sf.radius = 1
		sf.maxSpeed = (28369*angle^5)/2088450000-(2396963*angle^4)/1392300000+(9425711*angle^3)/119340000-(42493891*angle^2)/27846000+(879136*angle)/116025+265
		sf.levelFlight = False

	def pc(sf,fDat,fCmd):
		condition = False
		if(sf.alchange > 6000 or sf.alchange < -2000):
			print('WARNING:Altitude change too large!')

		if(sf.destSpeed > 260 ):
			print('speed too fast, round it down to 250')
			condition = True
			sf.destSpeed = 250
		if(sf.destAngle > 65):
			condition = True
			sf.destAngle = 70
		if(sf.destAngle < -65):
			condition = True
			sf.destAngle = -65

		if(sf.alchange * sf.destAngle < 0):
			print('it is not possible to climb/des when the degree has the opposite sign ',sf.alchange * sf.destAngle)
			condition = True
			if(alchange > 0):
				sf.destAngle = 5
				#return (5,sf.destSpeed)#angle and speed
			else:
				sf.destAngle = -5
				#return (-5,sf.destSpeed)

		if(sf.destSpeed < 95):
			sf.destSpeed = 95
			condition = True
			#return (sf.destAngle,90)

		if(sf.destSpeed > sf.maxSpeed and sf.alchange >= 0):
			print('speed too fast for this angle, but still can reach')

		if condition :
			return (sf.destAngle,sf.destSpeed)
		else:
			return 'OK'

	def plan(sf,fDat,fCmd):
		pass

	def do(sf,fDat,fCmd):
		if(sf.prevTime == fDat.time): #if the same package, skip
			return True
		else:
			curTime = fDat.time
			timeDiff = fDat.time-sf.prevTime
			curLocation = [fDat.latitude, fDat.longitude]
			curAlt = fDat.altitude
			#print('curLocation', curLocation)
			print('altitude',curAlt)
			print('final Alt',sf.alchange+2000)

			roll = fDat.roll
			speed = fDat.kias
			print('roll: ',roll)
			print('kias: ', speed)
			print('finalKias: ',sf.destSpeed)


			groudDist = Pdist(curLocation, sf.prevLocation)
			altDist = curAlt - sf.prevAltitude
			Altchange = curAlt - sf.altitude # curr - 2000(start al)
			if groudDist != 0 :
				degree = math.degrees(math.atan(altDist/groudDist))
				print('climb/des degree: ',degree)


			curPitch = fDat.pitch # pitch (angle)
			destAngle = sf.destAngle
			print('pitch: ', curPitch)
			print('dest climb/des degree: ', destAngle)

			if(curTime - sf.startTime < 8):
				if groudDist != 0 :
					pitchPIDRet = sf.pitchPID.pid(0 - degree,timeDiff)
					print('pitchPID return: ', pitchPIDRet)
					fCmd.elevator = pitchPIDRet
			else:
				if groudDist != 0 :
					pitchPIDRet = sf.pitchPID.pid(sf.destAngle - degree,timeDiff)
					print('pitchPID return: ', pitchPIDRet)
					fCmd.elevator = pitchPIDRet

			speedPIDRet = sf.speedPID.pid(sf.destSpeed-speed,timeDiff)
			print('speedPID return: ', speedPIDRet)
			fCmd.throttle = speedPIDRet

			# COMMENT OUT THESE LINE IF DONT WANT ROLL!!!
			if(curTime - sf.startTime < 3.5):
				#rollPIDRet = sf.rollPID.pid(sf.roll-roll,timeDiff)
				#print('rollPID return: ', rollPIDRet)
				#if sf.roll < 165:
				fCmd.aileron = 1
				#else :
				#	pass
					#fCmd.aileron = -1
			else:
				rollPIDRet = sf.rollPID.pid(sf.roll-roll,timeDiff)
				print('rollPID return: ', rollPIDRet)
				fCmd.aileron = rollPIDRet

			print('aileron:',fCmd.aileron)
			print('elevator:',fCmd.elevator)
			print('throttle:',fCmd.throttle)

			print('===========================================')

			if(sf.destSpeed < 200  and speed > sf.destSpeed+35):
				sf.speedPID.pidClear()

			if( abs(Altchange - sf.alchange) < 100 ):
				print('start level flight')
				sf.levelFlight = True
				sf.destAngle = 0 # level flight
			if( abs(Altchange - sf.alchange) > 100 and sf.levelFlight):
				if Altchange < sf.alchange:
					sf.destAngle = 5 #
				else: # higher than the final Alt
					sf.destAngle = - 5



			if( abs(Altchange - sf.alchange) < 100 and abs(speed - sf.destSpeed) < 20 and abs(degree) < 3 ):
				print('++++++++++++++++++++++++')
				sf.speedPID.pidClear()
				sf.pitchPID.pidClear()
				sf.rollPID.pidClear()
				return 'DONE'

			#update variables
			if sf.firstRun:
				sf.startTime = fDat.time
				sf.firstRun = False
			sf.prevTime = fDat.time
			sf.prevLocation = curLocation
			sf.prevAltitude = curAlt
			return





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
