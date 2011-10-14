
from collections import namedtuple

class NoSolutionError(Exception):
    pass

Action = namedtuple ('Action', ['gotoState',])
Neighbor = namedtuple("Neighbor", ["cost", "state"])
Node = namedtuple ('Node', ['action', 'cost', 'parent', 'state'])

class Problem(object):
    """Defines the problem space or node list.

    A node is a decision point.
    """
    def __init__ (self, finalState, initialState, strategy):
        object.__init__ (self)
        self.__finalState = finalState
        self.__initialState = initialState
        self.__strategy = strategy
        return

    def actions (self, state):
        return

    def heuristic (self, state, action):
        return self.__strategy._heuristic (state, action)
    
    def goalTest (self, state):
        return state == self.__finalState

    def initialState (self):
        return self.__initialState

    def stepCost (self, state, action):
        return self.__strategy._stepCost (state, action)
    pass

class BreadthFirstStrategy(object):
    def _heuristic (self, state, action):
        return 0

    def _stepCost (self, state, action):
        return 1
    pass

class UniformCostStrategy(object):
    def __init__ (self, costFunc):
        object.__init__ (self)
        self.__costFunc = costFunc
        return

    def _heuristic (self, state, action):
        return 0

    def _stepCost (self, state, action):
        return self.__costFunc (state, action)
    pass

def find (problem, verbose=False):
    complete = False
    explored = {}
    frontier = { problem.initialState():Node(None, 0, None,
                                             problem.initialState()), }
    solution = None
    while not complete:
        if len (frontier) == 0:
            raise NoSolutionError("Exhausted the frontier without finding " +
                                  "the goal!")

        # watch the search happen...
        if verbose:
            for n in frontier.values():
                print problem.expand (n) + " (" + str (n.cost) + ")"
                pass
            print "----"
            pass
        
        # find the lowest cost element
        min = frontier.values()[0]
        for n in frontier.itervalues():
            if n.cost < min.cost: min = n
            pass

        # remove the lowest cost element from the tree and add it to the
        # explored list
        node = frontier.pop (min.state)
        explored[node.state] = node

        # check to see if goal state and exit
        if problem.goalTest (node.state):
            solution = node
            break

        # loop over all actions from a given state
        for a in problem.actions (node.state):
            # ignore states that have already been visited
            if a.gotoState in explored: continue

            # compute the new cost and generate a new node
            evaluation = problem.stepCost (node.state, a) + \
                         problem.heuristic (node.state, a)
            cost = node.cost + evaluation
            next = Node (action=a, cost=cost,
                         parent=node, state=a.gotoState)

            # if it is in the frontier but the other path is cheaper then
            # continue on forgetting this path, otherwise replace the other
            # path with this one
            if a.gotoState in frontier and \
               frontier[a.gotoState].cost < next.cost: continue
            
            frontier[next.state] = next
            pass
        pass
    return solution

