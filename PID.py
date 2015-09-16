import imp, sys
import Ckpt as Ckpt

class PID ():

	def __init__(sf,coeffP,coeffI,coeffD):
		sf.cumError = 0
		sf.coeffP = coeffP
		sf.coeffI = coeffI
		sf.coeffD = coeffD
		sf.lastError = 0

	def pid(sf,error,time):
		sf.cumError += error
		ret = error*sf.coeffP + (sf.cumError*time)*sf.coeffI + (sf.lastError-error)/time*sf.coeffD

		print("P:",error*sf.coeffP)
		print("I:",(sf.cumError*time)*sf.coeffI )
		print("time:", time )
		print("cumError:", (sf.cumError*time) )
		print("D:",(sf.lastError-error)/time*sf.coeffD)

		sf.lastError = error
		return ret
		
	def pidClear(sf):
		sf.cumError = 0
