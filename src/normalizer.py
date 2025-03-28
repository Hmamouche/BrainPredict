import pandas as pd
import numpy as np
import pickle

class normalizer:
	"""
		Specific normalisation of a pandas dataframe
		Order of features doesn't matter
	"""

	#----------------------------------#
	def __init__ (self, df = pd.DataFrame ()):
		self. features = list (df. columns)
		self. minMax = {}

		if not df. empty:
			for feature in df. columns:
				self. minMax [feature] = [df. loc [:, feature]. min (), df. loc [:, feature]. max ()]

	#----------------------------------#
	@staticmethod
	def normalize (vect, minMax):
		""" Normalizing a vector based using min-max values
		Parameters
		----------
		vect: {'list', 'ndarray'}
			lis of numpy array of 1 dimension
		minMax: list
			list 'of 2 elements, i.e., min and max scalers """
		for i in range (len (vect)):
			vect [i] = (vect[i] - minMax[0]) / float(minMax[1] - minMax[0])
		return vect

	#----------------------------------#
	def transform (self, df_):
		df = df_. copy (). astype (float)
		for feature in df. columns:
			if feature in self. features:
				df [feature] = self. normalize (df.loc [:,feature]. values, self. minMax [feature])

		return df

	#----------------------------------#
	def save (self, filename):
		pickle_filename = open ("%s.pickle"%filename.split ('.')[0],"wb")
		pickle. dump (self. minMax, pickle_filename)
		pickle_filename.close()

	#------------------------------------#
	def load (self, filename):
		pickle_in = open(filename,"rb")
		self. minMax = pickle. load (pickle_in)
		self. features = self. minMax. keys ()
