# defines a vector class to represent the states and transitions
import random


class markov_vector:
    def __init__(self):
        self.transitionCounts = dict()
        self.transitionsPerState = dict()

    # add an state or beef up probability

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
    # function: generateTransition(state)

    def build_from_file(self, fileName):
        with open(fileName) as fileData:
            content = fileData.readlines()
        for line in content:
            # don't try to add states from an empty line
            if len(line) < 3:
                break
            words = line.split()
            self.add_state("NULL", words[0])
            for i in xrange(len(words)-2):
                self.add_state(words[i], words[i+1])
            self.add_state(words[-1], None)

    def generateTransition(self, state):
        if state not in self.transitionCounts:
            return None
        while True:
            for transition in self.transitionCounts[state]:
                if (float(self.transitionCounts[state][transition]) /
                   self.transitionsPerState[state]) > random.random():
                    return transition
