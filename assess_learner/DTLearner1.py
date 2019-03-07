import numpy as np

class DTLearner(object):

	def __init__(self, leaf_size = 1, verbose = False):
		self.leaf_size = leaf_size
		self.verbose = verbose	
		pass # move along, these aren't the drones you're looking for  

	def author(self):
		return 'swang632' # replace tb34 with your Georgia Tech username
    
	def addEvidence(self, Xtrain, Ytrain):
		data = np.column_stack((Xtrain, Ytrain))
		self.tree = self.build_tree(data)		

	def build_tree(self, data):
		if data.shape[0] == 1:
			return np.array([["Leaf", np.mean(data[:,-1]), "NA", "NA"]], dtype=object)
		elif data.shape[0] <= self.leaf_size:
			return np.array([["Leaf", np.unique(data[:,-1])[0], "NA", "NA"]], dtype=object)
		else:
			i, split_val, left, right = self.selectfeature(data)
			if np.array_equal(left, data) == True:
				return np.array([["Leaf", np.mean(data[:,-1]), "NA", "NA"]], dtype=object)
			left_tree = self.build_tree(left)
			right_tree = self.build_tree(right)
			root = np.array([i, split_val, 1, left_tree.shape[0] + 1])
			return np.vstack([root, left_tree, right_tree])
	
	def selectfeature(self, data):
		i = 0
		temp = 0
		length = data.shape[1] - 1
		for j in range(length):
			if np.correlate(data[:,j],data[:,-1]) > temp:
				temp = np.correlate(data[:,j], data[:,-1])
				i = j
		split_val = np.median(data[:,i])
		left = data[data[:, i] <= split_val]
		right = data[data[:, i] > split_val]		
		return i, split_val, left, right
	
	def query(self, Xtest):
		length = Xtest.shape[0]
		self.outputs = []
		for i in range(length):
			self.query_value(Xtest[i], 0)
		return np.array(self.outputs)
    
	def query_value(self, Xtest, index):
		result = self.tree[index,:]
		if result[0] == 'Leaf':
			self.outputs.append(result[1])
		elif Xtest[result[0]] <= result[1]:
			self.query_value(Xtest, index + result[2])
		elif Xtest[result[0]] > result[1]:
			self.query_value(Xtest, index + result[3])

			
if __name__=="__main__":
	print ("This is a DT Learner\n")
