import numpy as np
import DTLearner as dt
import RTLearner as rt
import LinRegLearner as lr

class BagLearner(object):

	def __init__(self, learner = {}, kwargs = {}, bags = 20, boost = False, verbose = False):
		self.learners = []
		self.bags = bags
		self.boost = boost
		self.verbose = verbose
		self.kwargs = kwargs			
		for i in range(0, bags):
			self.learners.append(learner(**kwargs))
		pass # move along, these aren't the drones you're looking for  
	
	def author(self):
		return 'swang632' # replace tb34 with your Georgia Tech username
	
	def addEvidence(self, Xtrain, Ytrain):
		for i in range(0, self.bags):
			self.learners[i].addEvidence(Xtrain, Ytrain)
		
	def query(self, Xtest):
		self.outputs = []
		for i in range(0, self.bags):
			self.outputs.append(self.learners[i].query(Xtest))
		return np.mean(self.outputs, axis = 0)
	
	
if __name__=="__main__":
	print ("This is a Bag Learner\n")
