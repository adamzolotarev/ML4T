"""Assess a betting strategy.  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
Copyright 2018, Georgia Institute of Technology (Georgia Tech)  		   	  			    		  		  		    	 		 		   		 		  
Atlanta, Georgia 30332  		   	  			    		  		  		    	 		 		   		 		  
All Rights Reserved  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
Template code for CS 4646/7646  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
Georgia Tech asserts copyright ownership of this template and all derivative  		   	  			    		  		  		    	 		 		   		 		  
works, including solutions to the projects assigned in this course. Students  		   	  			    		  		  		    	 		 		   		 		  
and other users of this template code are advised not to share it with others  		   	  			    		  		  		    	 		 		   		 		  
or to make it available on publicly viewable websites including repositories  		   	  			    		  		  		    	 		 		   		 		  
such as github and gitlab.  This copyright statement should not be removed  		   	  			    		  		  		    	 		 		   		 		  
or edited.  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
We do grant permission to share solutions privately with non-students such  		   	  			    		  		  		    	 		 		   		 		  
as potential employers. However, sharing with other current or future  		   	  			    		  		  		    	 		 		   		 		  
students of CS 7646 is prohibited and subject to being investigated as a  		   	  			    		  		  		    	 		 		   		 		  
GT honor code violation.  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
-----do not edit anything above this line---  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
Student Name: Tucker Balch (replace with your name)  		   	  			    		  		  		    	 		 		   		 		  
GT User ID: swang632 (replace with your User ID)
GT ID: 903270437 (replace with your GT ID)
"""  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt

def author():
    return 'swang632' # replace tb34 with your Georgia Tech username.

def gtid():
    return 903270437 # replace with your GT ID number

def get_spin_result(win_prob):
    
    result = False
    if np.random.random() <= win_prob:
        result = True
    return result

def test_code():
    win_prob = 0.60
    np.random.seed(gtid())
    print get_spin_result(win_prob)

# add your code here to implement the experiments
def experiment1_simulator():
    player_win = 0.00
    max_player_win = 80.00
    max_spin_count = 1000
    outcome = np.full(max_spin_count+1, max_player_win)
    outcome[0] = 0
    count = 0
    while (player_win < max_player_win) and (count < max_spin_count):
        won = False
        bet_amount = 1.00
        while (won == False) and (count<max_spin_count):
            prob = 18.0/38.0
            won = get_spin_result(prob)
            if won == True:
                player_win = player_win + bet_amount
            else:
                player_win = player_win - bet_amount
                bet_amount = bet_amount*2
            count += 1
            outcome[count] = player_win
    return outcome

def experiment2_simulator():
    player_win = 0.00
    max_player_win = 80.00
    player_bankroll = 256.00
    max_spin_count = 1000
    outcome = np.full(max_spin_count+1,max_player_win)
    outcome[0] = 0
    count = 0
    while (player_win<max_player_win) and (count < max_spin_count):
        won = False
        bet_amount = 1.00
        while (won == False) and (count < max_spin_count):
            prob = 18.0/38.0
            won = get_spin_result(prob)
            if won == True:
                player_win = player_win + bet_amount
            else:
                player_win = player_win - bet_amount
                if bet_amount * 2 > player_win + player_bankroll:
                    bet_amount = player_win + player_bankroll
                else:
                    bet_amount = bet_amount * 2
            count += 1
            outcome[count] = player_win
            if player_win <= -256:
                break;
        if player_win <= -player_bankroll:
            outcome[count+1:] = -player_bankroll
            break;
    return outcome


if __name__ == "__main__":
    Path = './'
    count = 1
    while count <= 10:
        plt.plot(experiment1_simulator())
        count += 1
    plt.xlim(0,300)
    plt.ylim(-256,100)
    plt.xlabel('Number of Spins')
    plt.ylabel('Win(Lost) Amount')
    plt.title('Figure 1')
    plt.savefig(Path + 'Figure1.png')
    plt.close()

    result = experiment1_simulator()
    count = 1
    while count < 1000:
        result = np.row_stack((result, experiment1_simulator()))
        count += 1
    mean = np.mean(result, axis = 0)
    std = np.std(result, axis = 0)
    plt.plot(mean, label='Mean')
    plt.plot(mean + std,label = 'Mean + Std')
    plt.plot(mean - std,label = 'Mean - Std' )
    plt.legend(loc = 'lower right')
    plt.xlim(0,300)
    plt.ylim(-256,100)
    plt.xlabel('Number of Spins')
    plt.ylabel('Win(Lost) Amount')
    plt.title('Figure 2')
    plt.savefig(Path + 'Figure2.png')
    plt.close()

    median = np.median(result, axis = 0)
    plt.plot(median, label = 'Median')
    plt.plot(median + std,label = 'Median + Std')
    plt.plot(median - std,label = 'Median - Std')
    plt.legend(loc = 'lower right')
    plt.xlim(0,300)
    plt.ylim(-256,100)
    plt.xlabel('Number of Spins')
    plt.ylabel('Win(Lost) Amount')
    plt.title('Figure 3')
    plt.savefig(Path + 'Figure3.png')
    plt.close()

    real_result = experiment2_simulator()
    count = 1
    while count < 1000:
        real_result = np.row_stack((real_result, experiment2_simulator()))
        count += 1
    real_mean = np.mean(real_result, axis = 0)
    real_std = np.std(real_result, axis = 0)
    plt.plot(real_mean, label = 'Mean')
    plt.plot(real_mean + real_std, label = 'Mean + Std')
    plt.plot(real_mean - real_std, label = 'Mean - Std')
    plt.legend(loc = 'lower left')
    plt.xlim(0,300)
    plt.ylim(-256,100)
    plt.xlabel('Number of Spins')
    plt.ylabel('Win(Lost) Amount')
    plt.title('Figure 4')
    plt.savefig(Path + 'Figure4.png')
    plt.close()

    real_median = np.median(real_result, axis = 0)
    plt.plot(real_median, label = 'Median')
    plt.plot(real_median + real_std, label = 'Median + Std')
    plt.plot(real_median - real_std, label = 'Median - Std')
    plt.legend(loc = 'lower left')
    plt.xlim(0,300)
    plt.ylim(-256,100)
    plt.xlabel('Number of Spins')
    plt.ylabel('Win(Lost) Amount')
    plt.title('Figure 5')
    plt.savefig(Path + 'Figure5.png')
    plt.close()

final_result = result[:,1000]
result_freq1 = pd.value_counts(pd.Series(final_result))
print 'Experiment 1 winning probability: %.3f' % ((result_freq1[80.0])/1000.00)
final_result = real_result[:,1000]
result_freq = pd.value_counts(pd.Series(final_result))
print 'Experiment 2 winning probability: %.3f' % ((result_freq[80.0])/1000.00)
print 'Mean winning for experiment 2: %0.3f' % np.mean(final_result)
