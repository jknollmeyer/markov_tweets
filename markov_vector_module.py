# defines a vector class to represent the states and transitions


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
        else:
            self.transitionCounts[state] = dict({transition: 1})

    # function: generateTransition(state)
