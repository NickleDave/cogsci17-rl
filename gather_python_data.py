# Runs the pure python model a bunch of times and prints to a file that can be plotted with pandas

from __future__ import print_function  # Only needed for Python 2
from daw_mbf_1 import Agent
from calcStayProb import CalcStayProb
import sys
import time

num_runs = 20#100
num_steps = 1000#40000
tf_name = 'temp_file.txt'

# Read option parameters from the command line
if len(sys.argv) == 3:
    num_runs = int(sys.argv[1])
    num_steps = int(sys.argv[2])
if len(sys.argv) == 2:
    num_runs = int(sys.argv[1])

for alpha in [.3]:#[0.01,0.05, 0.1, .2, .3]:
    outfile_name = 'data/out_py_a{0}_r{1}_s{2}.txt'.format(alpha, num_runs, num_steps)
    with open(outfile_name, 'w+') as outfile:

        for i in range(num_runs):
            print('{0}/{1} Runs'.format(i,num_runs))

            # w+ makes sure this file gets overwritten each time
            with open(tf_name, 'w+') as tf:
                agent = Agent()

                #print "firstStageChoice secondStage secondStageChoice finalReward"
                firstStageChoice = None
                secondStage = None
                secondStageChoice = None
                finalReward = None
                for step in range(num_steps): # Repeat (for each step of episode):
                    if agent.oneStep() == None:
                        print ("oneStep broke")
                        break
                    if step%2 == 0: # in stage 1
                        firstStageChoice = agent.getLastAction()
                        secondStage = agent.getCurrBoardState()
                    else: # in stage 2
                        secondStageChoice = agent.getLastAction()
                        finalReward = agent.getCurrReward()
                        print('{0} {1} {2} {3}'.format(firstStageChoice, secondStage, secondStageChoice, finalReward), file=tf)


                calculator = CalcStayProb()
                calculator.doItAll(tf_name, outfile)
