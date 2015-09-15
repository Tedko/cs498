import imp, sys
import Ckpt as Ckpt

class PID ():

	def __init__(sf,coeffP,coeffI,coeffD):
		sf.cumError = 0
		sf.coeff = coeff

	def pid(sf,error,time):
		sf.cumError += error
		return error*sf.coeffP + (sf.cumError/time)*sf.coeff

	def pidClear(sf):
		sf.cumError = 0
