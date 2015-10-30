import Ckpt
import imp, sys
import math
import PID

try: from . import Utilities, Fgfs							# being run from parent directory
except SystemError: import Utilities, Fgfs		# being run from ClassCode


class Planner:

	def __init__(sf,angle,alchange,finalspeed):
		sf.prevTime = 0.0
		sf.speedPID = PID.PID( 0.05,0.0008,0.01 )
		sf.rollPID = PID.PID( 0.002,0.002,0.001 )
		sf.pitchPID = PID.PID( -0.009,-0.001,-0.0001 )#pitch 1 goes down
		sf.destSpeed = finalspeed
		sf.destSpeedcp = finalspeed
		sf.roll = 0
		sf.altitude = 2000
		sf.prevAltitude = 2000
		sf.prevLocation = [37.613555908203125, -122.35719299316406]
		sf.alchange = alchange
		sf.destPitch = angle
		sf.destPitchcp = angle
		sf.radius = 1
		sf.maxSpeed = (28369*angle^5)/2088450000-(2396963*angle^4)/1392300000+(9425711*angle^3)/119340000-(42493891*angle^2)/27846000+(879136*angle)/116025+265


	def pc(sf,fDat,fCmd):
		if(sf.alchange > 7000 or sf.alchange < -2000):
			print('Altitude change too large!')
			#return False

		if(sf.alchange * sf.destPitch < 0):
			print('it is not possible to climb/des when the degree has the opposite sign ',sf.alchange * sf.destPitch)
			if(alchange > 0):
				return (1,sf.finalspeed)#angle and speed
			else:
				return (-1,sf.finalspeed)

		if(sf.destSpeed < 0):
			print('non positive speed! Please enter meaningful speed.')
			return (sf.destPitch,250)

		if(sf.destSpeed > 260 ):
			print('speed too fast, round it down to 250')
			sf.destSpeed = 250
			return (sf.destPitch,250)
		if(sf.destSpeed > sf.maxSpeed and sf.alchange >= 0):
			print('speed too fast for this angle')

		return 'OK'


	def plan(sf,fDat,fCmd):

		if(sf.alchange > 7000):
			print('Altitude change too large!')
			return False

		if(sf.alchange * sf.destPitch < 0):
			print('it is not possible to climb/des when the degree has the opposite sign ',sf.alchange * sf.destPitch)
			return False

		if(sf.destSpeed < 0):
			print('non positive speed! Please enter meaningful speed.')
			return False

		if(sf.destSpeed > 260 ):
			print('speed too fast, round it down to 250')
			sf.destSpeed = 250
		if(sf.destSpeed > sf.maxSpeed and sf.alchange >= 0):
			print('speed too fast for this angle, program will try to climb first')
		#double check!


	#def do(sf,fDat,fCmd)
		if(sf.prevTime == fDat.time): #if the same package, skip
			return True
		else:
			timeDiff = fDat.time-sf.prevTime
			curLocation = [fDat.latitude, fDat.longitude]
			curAlt = fDat.altitude
			print('curLocation', curLocation)
			print('altitude',curAlt)
			print('needed Altchange',sf.alchange)

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
			destPitch = sf.destPitch
			print('pitch: ', curPitch)
			print('dest climb/des degree: ', destPitch)

			if groudDist != 0 :
				pitchPIDRet = sf.pitchPID.pid(sf.destPitch - degree,timeDiff)
				print('pitchPID return: ', pitchPIDRet)
				fCmd.elevator = pitchPIDRet


			speedPIDRet = sf.speedPID.pid(sf.destSpeed-speed,timeDiff)
			rollPIDRet = sf.rollPID.pid(sf.roll-roll,timeDiff)
			print('speedPID return: ', speedPIDRet)
			print('rollPID return: ', rollPIDRet)

			fCmd.throttle = speedPIDRet


			fCmd.aileron = rollPIDRet
			print('aileron:',fCmd.aileron)
			print('elevator:',fCmd.elevator)
			print('throttle:',fCmd.throttle)

			print('===========================================')



			if( abs(Altchange - sf.alchange) < 100 ):
				print('start level flight')
				sf.destPitch = 0 # level flight
			if( abs(Altchange - sf.alchange) > 100 ):
				sf.destPitch = sf.destPitchcp # level flight


			if( abs(Altchange - sf.alchange) < 100 and abs(speed - sf.destSpeed) < 20 ):
				print('++++++++++++++++++++++++')
				print('DONE')
				sf.speedPID.pidClear()
				sf.pitchPID.pidClear()
				sf.rollPID.pidClear()
				return False


			#update variables
			sf.prevTime = fDat.time
			sf.prevLocation = curLocation
			sf.prevAltitude = curAlt
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
