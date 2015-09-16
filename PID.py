import imp, sys
import Ckpt as Ckpt

class PID ():

	def __init__(sf,coeffP,coeffI,coeffD):
		sf.cumError = 0
		sf.coeffP = coeffP
		sf.coeffI = coeffI
		sf.coeffD = coeffD
		sf.prevError = 0
	def pid(sf,error,timeDiff):
		sf.cumError += error
		derivative = (sf.prevError-error)/timeDiff
		#print("diri :",derivative)
		integral = sf.cumError*timeDiff*0.9
		ret = error*sf.coeffP + integral*sf.coeffI + derivative*sf.coeffD
		print("cumError:", (sf.cumError*timeDiff) )
		print("P:",error*sf.coeffP )
		print("I:",integral*sf.coeffI )
		print("D:",derivative*sf.coeffD )

		sf.prevError = error
		return ret

	def pidClear(sf):
		sf.cumError = 0
