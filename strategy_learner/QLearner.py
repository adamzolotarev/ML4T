"""
    Template for implementing QLearner  (c) 2015 Tucker Balch
    
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
    
    Student Name: Sihao Wang (replace with your name)
    GT User ID: swang632 (replace with your User ID)
    GT ID: 903270437 (replace with your GT ID)
    """

import numpy as np
import random as rand

class QLearner(object):

    def __init__(self, \
        num_states = 100, \
        num_actions = 4, \
        alpha = 0.2, \
        gamma = 0.9, \
        rar = 0.5, \
        radr = 0.99, \
        dyna = 0, \
        verbose = False):

        self.verbose = verbose
        self.num_states = num_states
        self.num_actions = num_actions
        self.alpha = alpha
        self.gamma = gamma
        self.rar = rar
        self.radr = radr
        self.dyna = dyna
        self.s = 0
        self.a = 0
        self.q_table = np.random.uniform(-1.0, 1.0, size=(num_states,num_actions))
        self.V = []


        if (self.dyna!=0):
            self.Tcount = np.ndarray(shape=(self.num_states, self.num_actions, self.num_states))
            self.Tcount.fill(0.0001)
            self.T = self.Tcount/self.Tcount.sum(axis=2,keepdims=True)
            self.R = np.ndarray(shape=(self.num_states, self.num_actions))
            self.R.fill(-1.0)


    def querysetstate(self, s):
        """
        @summary: Update the state without updating the Q-table
        @param s: The new state
        @returns: The selected action
        """
        self.s = s
        if (rand.random() < self.rar):
            rand.seed(1)
            action = rand.randint(0, self.num_actions-1)
        else:
            action = np.argmax(self.q_table[s,:])
            self.rar *= self.radr
        if self.verbose: print "s =", s,"a =",action
        return action

    def query(self,s_prime,r):
        """
        @summary: Update the Q table and return an action
        @param s_prime: The new state
        @param r: The ne state
        @returns: The selected action
        """
        action = np.argmax(self.q_table[s_prime,:])
        self.q_table[self.s, self.a] = (1 - self.alpha) * self.q_table[self.s, self.a] + self.alpha * (r + self.gamma * np.max(self.q_table[s_prime,action]))
        count = self.dyna
        self.V.append((self.s,self.a,s_prime,r))
        while(count):
            index = rand.randint(0,len(self.V)-1)
            s_current,a_current,s_next,r_next = self.V[index]
            a_next = np.argmax(self.q_table[s_next,:])
            self.q_table[s_current,a_current] = (1.0-self.alpha) * self.q_table[s_current,a_current] + self.alpha * (r_next + self.gamma * self.q_table[s_next,a_next])
            count -= 1

        action = np.argmax(self.q_table[s_prime, :])
        if rand.random() < self.rar:
            action = rand.randint(0, self.num_actions - 1)
            self.rar = self.rar * self.radr
        self.a = action
        self.s = s_prime
        if self.verbose: print "s =", s_prime,"a =",action,"r =",r
        return action

    def author(self):
        return 'swang632'


if __name__=="__main__":
    print "Remember Q from Star Trek? Well, this isn't him"
