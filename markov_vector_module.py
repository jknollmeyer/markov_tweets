# defines a vector class to represent the states and transitions
import random


class markov_vector:
    def __init__(self):
        self.transitionCounts = dict()
        self.transitionsPerState = dict()

    # add a possible transition or raise the weight of a current one
    def add_state(self, state, transition):
        if state in self.transitionCounts:
            if transition in self.transitionCounts[state]:
                self.transitionCounts[state][transition] += 1
            else:
                self.transitionCounts[state][transition] = 1
            self.transitionsPerState[state] += 1
        else:
            self.transitionCounts[state] = dict({transition: 1})
            self.transitionsPerState[state] = 1

    def build_from_corpus(self, content):
        for line in content.splitlines():
            words = line.split()
            # omit lines which are too short to process
            if len(words) < 5:
                continue

            # special cases for beginnings
            self.add_state((None, None), words[0])
            self.add_state((None, words[0]), words[1])

            # add all transitions for a 2-tuple and the following word
            for i in xrange(0, len(words)-3):
                self.add_state((words[i], words[i+1]), words[i+2])

            # special cases for endings
            self.add_state((words[len(words)-2], words[len(words)-1]),
                           None)
            self.add_state((words[len(words)-1], None), None)

            # old code for states with a size of only 1
            ''''
            self.add_state("NULL", words[0])
            for i in xrange(len(words)-2):
                self.add_state(words[i], words[i+1])
            self.add_state(words[-1], None)
            '''

    # given a current state, randomly generate the next state
    def generateTransition(self, state):
        if state not in self.transitionCounts:
            return None
        while True:
            for transition in self.transitionCounts[state]:
                if (float(self.transitionCounts[state][transition]) /
                   self.transitionsPerState[state]) > random.random():
                    return transition
