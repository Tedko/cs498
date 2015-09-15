import imp, sys
import Ckpt as Ckpt

class PID ():

	def __init__(sf,coeff):
		sf.cumError = 0
		sf.coeff = coeff

	def pid(sf,error,time):
		sf.cumError += error
		return error*(sf.cumError/time)*sf.coeff

	def pidClear(sf):
		sf.cumError = 0
