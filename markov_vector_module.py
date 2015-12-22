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

    def generateTransition(self, state):
        if state not in self.transitionCounts:
            return None
        while True:
            for transition in self.transitionCounts[state]:
                if (float(self.transitionCounts[state][transition]) /
                   self.transitionsPerState[state]) > random.random():
                    return transition
