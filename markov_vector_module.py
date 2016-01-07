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

    def build_from_corpus(self, content, chainLength):
        for line in content.splitlines():
            words = line.split()
            # omit lines which are too short to process
            if len(words) < chainLength:
                continue

            # special cases for beginnings
            stateList = [None] * chainLength
            index = 0
            while stateList[0] is None:
                self.add_state(tuple(stateList), words[index])
                stateList = stateList[1:] + [words[index]]
                index += 1
            while index < len(words):
                self.add_state(tuple(stateList), words[index])
                stateList = stateList[1:] + [words[index]]
                index += 1
            while stateList[0] is not None:
                self.add_state(tuple(stateList), None)
                stateList = stateList[1:] + [None]


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
