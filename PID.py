import imp, sys
import Ckpt as Ckpt

class PID ():

	def __init__(sf,coeffP,coeffI,coeffD):
		sf.coeffP = coeffP
		sf.coeffI = coeffI
		sf.coeffD = coeffD
		sf.prevError = 0
	def pid(sf,error,timeDiff):
		derivative = (error-sf.prevError)/timeDiff
		integral = (sf.prevError+error)*timeDiff/2*0.9
		ret = error*sf.coeffP + integral*sf.coeffI + derivative*sf.coeffD
		print("P:",error*sf.coeffP )
		print("I:",integral*sf.coeffI )
		print("D:",derivative*sf.coeffD )

		sf.prevError = error
		return ret

	def pidClear(sf):
		sf.cumError = 0
