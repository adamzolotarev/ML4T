import util
import numpy as np
import math
import DTLearner as dt
import RTLearner as rt
import BagLearner as bl
import sys
import matplotlib.pyplot as plt
import time
import scipy.stats as stats

if __name__=="__main__":
    Path = './'
    if len(sys.argv) != 2:
        print "Usage: python testlearner.py <filename>"
        sys.exit(1)
    
    datafile = sys.argv[1]
    data = np.genfromtxt(util.get_learner_data_file(datafile),delimiter=',')

    if datafile == 'Istanbul.csv':
        data = data[1:,1:]

    datasize = data.shape[0]
    cutoff = int(datasize*0.6)
    leaf_sizes = range(1,51)

#Problem 1

    rmse_in = np.zeros((len(leaf_sizes),5))
    rmse_out = np.zeros((len(leaf_sizes),5))
    ind = 0
    
    for leaf_size in leaf_sizes:
        
        permutation = np.random.permutation(data.shape[0])
        col_permutation = np.random.permutation(data.shape[1]-1)
        train_data = data[permutation[:cutoff],:]
        trainX = train_data[:,col_permutation]
        trainY = train_data[:,-1]
        test_data = data[permutation[cutoff:],:]
        testX = test_data[:,col_permutation]
        testY = test_data[:,-1]
        for trials in range(5):
            learner = dt.DTLearner(leaf_size = leaf_size, verbose = False)
            learner.addEvidence(trainX, trainY)
            predY = learner.query(trainX)
            rmse_in[ind, trials] = np.sqrt(((trainY - predY)**2).mean())
            predY = learner.query(testX)
            rmse_out[ind, trials] = np.sqrt(((testY - predY)**2).mean())
        ind += 1

    plt.plot(leaf_sizes,np.mean(rmse_in, axis = 1), '--', label = 'In Sample RMSE')
    plt.plot(leaf_sizes,np.mean(rmse_out, axis = 1), label = 'Out of Sample RMSE')
    plt.legend(loc='lower right')
    plt.xlabel('Leaf Size')
    plt.ylabel('RMSE')
    plt.title('DtLearner:Leaf size vs RMSE')
    plt.savefig(Path + 'Figure1.png')
    plt.close()



#problem 2
    rmse_in = np.zeros((len(leaf_sizes),5))
    rmse_out = np.zeros((len(leaf_sizes),5))
    ind = 0
    
    for leaf_size in leaf_sizes:
        
        permutation = np.random.permutation(data.shape[0])
        col_permutation = np.random.permutation(data.shape[1]-1)
        for trials in range(5):
    
    
            train_data = data[permutation[:cutoff],:]
            trainX = train_data[:,col_permutation]
            trainY = train_data[:,-1]
            test_data = data[permutation[cutoff:],:]
            testX = test_data[:,col_permutation]
            testY = test_data[:,-1]
            learner = bl.BagLearner(learner = dt.DTLearner, kwargs = {"leaf_size":leaf_size}, bags = 20, boost = False, verbose = False)
            learner.addEvidence(trainX, trainY)
            predY = learner.query(trainX)
            rmse_in[ind, trials] = np.sqrt(((trainY - predY)**2).mean())
            predY = learner.query(testX)
            rmse_out[ind, trials] = np.sqrt(((testY - predY)**2).mean())
        ind += 1
           


    plt.plot(leaf_sizes,np.mean(rmse_in, axis = 1), '--', label = 'In Sample RMSE')
    plt.plot(leaf_sizes,np.mean(rmse_out, axis = 1), label = 'Out of Sample RMSE')
    plt.legend(loc='lower right')
    plt.xlabel('Leaf Size')
    plt.ylabel('RMSE')
    plt.title('BagLearner: Leaf size vs RMSE')
    plt.savefig(Path + 'Figure2.png')
    plt.close()
    
    


#Problem 3

    rmse_out = np.zeros((len(leaf_sizes),5))
    rmse_out2 = np.zeros((len(leaf_sizes),5))
    corr_out = np.zeros((len(leaf_sizes),5))
    corr_out2 = np.zeros((len(leaf_sizes),5))
    time_out = np.zeros((len(leaf_sizes),5))
    time_out2 = np.zeros((len(leaf_sizes),5))
    ind = 0
    
    for leaf_size in leaf_sizes:
        
        permutation = np.random.permutation(data.shape[0])
        col_permutation = np.random.permutation(data.shape[1]-1)
        train_data = data[permutation[:cutoff],:]
        trainX = train_data[:,col_permutation]
        trainY = train_data[:,-1]
        test_data = data[permutation[cutoff:],:]
        testX = test_data[:,col_permutation]
        testY = test_data[:,-1]
        for trials in range(5):
            start_time = time.time()
            learner = dt.DTLearner(leaf_size = leaf_size, verbose = False)
            learner.addEvidence(trainX, trainY)
            time_out[ind, trials] = time.time() - start_time
            start_time = time.time()
            learner2 = rt.RTLearner(leaf_size = leaf_size, verbose = False)
            learner2.addEvidence(trainX, trainY)
            time_out2[ind, trials] = time.time() - start_time
            predY = learner.query(testX)
            predY2 = learner2.query(testX)
            rmse_out[ind, trials] = np.sqrt(((testY - predY)**2).mean())
            rmse_out2[ind, trials] = np.sqrt(((testY - predY2)**2).mean())
            corr_out[ind, trials] = stats.pearsonr(testY, predY)[0]
            corr_out2[ind, trials] = stats.pearsonr(testY, predY2)[0]
        ind += 1

    plt.plot(leaf_sizes,np.mean(rmse_out, axis = 1), '--', label = 'DTLearner')
    plt.plot(leaf_sizes,np.mean(rmse_out2, axis = 1), label = 'RTLearner')
    plt.legend(loc='lower right')
    plt.xlabel('Leaf Size')
    plt.ylabel('RMSE')
    plt.title('RMSE:DTlearner vs RTlearner')
    plt.savefig(Path + 'Figure3.png')
    plt.close()


    plt.plot(leaf_sizes,np.mean(corr_out, axis = 1), '--', label = 'DTLearner')
    plt.plot(leaf_sizes,np.mean(corr_out2, axis = 1), label = 'RTLearner')
    plt.legend(loc='lower right')
    plt.xlabel('Leaf Size')
    plt.ylabel('Correlation')
    plt.title('Correlation Coefficient:DTlearner vs RTlearner')
    plt.savefig(Path + 'Figure4.png')
    plt.close()



    plt.plot(leaf_sizes,np.mean(time_out, axis = 1), '--', label = 'DTLearner')
    plt.plot(leaf_sizes,np.mean(time_out2, axis = 1), label = 'RTLearner')
    plt.legend(loc='upper right')
    plt.xlabel('Leaf Size')
    plt.ylabel('Time')
    plt.title('Build Time:DTlearner vs RTlearner')
    plt.savefig(Path + 'Figure5.png')
    plt.close()

