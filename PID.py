import imp, sys
import Ckpt as Ckpt

class PID ():

	def __init__(sf,coeff):
		sf.cumError = 0
		sf.coeff = coeff
	def pid(error,time):
		sf.cumError += error
		return (cumError/time)*sf.coeff
