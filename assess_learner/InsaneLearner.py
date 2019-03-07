import numpy as np
import DTLearner as dt
import RTLearner as rt
import BagLearner as bl
import LinRegLearner as lr

class InsaneLearner(object):
    def __init__(self, bag_learner = bl.BagLearner, learner = lr.LinRegLearner, kwargs = {}, bags=20, boost=False, verbose=False):
        bag_learners = []
        for i in range(bags):
            bag_learners.append(bag_learner(learner, kwargs, bags))
        self.bag_learners = bag_learners
        self.boost = boost
        self.verbose = verbose
        self.kwargs = kwargs
        self.outputs = []
        pass # move along, these aren't the drones you're looking for  
    
    def author(self):
        return 'swang632' # replace tb34 with your Georgia Tech username
        
    def addEvidence(self, Xtrain, Ytrain):
        for learner in self.bag_learners:
            learner.addEvidence(Xtrain, Ytrain)
    
    def query(self, Xtest):
        for i in self.bag_learners:
            self.outputs.append(i.query(Xtest))
        return(np.average(self.outputs, axis=0))
    
if __name__=="__main__":
    print ("This is a Insane Learner\n")