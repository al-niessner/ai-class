
from general import Action
from general import BreadthFirstStrategy
from general import Neighbor
from general import Problem
from general import UniformCostStrategy

class TravelMap(Problem):
    def __init__ (self, strategy=None):
        Problem.__init__ (self,
                          finalState='b',
                          initialState='a',
                          strategy=self if strategy is None else strategy)
        self.__names = {
            'a':"Arad",
            'b':"Bucharest",
            'c':"Craiova",
            'd':"Drobeta",
            'e':"Eforie",
            'f':"Fagaras",
            'g':"Guirgui",
            'h':"Hirsova",
            'i':"Iasi",
            'l':"Lugoj",
            'm':"Mehadia",
            'n':"Neamt",
            'o':"Oradea",
            'p':"Pitesti",
            'r':"Rimnicu Vilcea",
            's':"Sibiu",
            't':"Timisoara",
            'u':"Urziceni",
            'v':"Vaslui",
            'z':"Zerind",
            }
        self.__neighbors = {
            'a':[Neighbor(75, 'z'),
                 Neighbor(141, 's'),
                 Neighbor(118, 't')],
            'b':[Neighbor(101, 'p'),
                 Neighbor(211, 'f'),
                 Neighbor(85, 'u'),
                 Neighbor(90, 'g')],
            'c':[Neighbor(120, 'd'),
                 Neighbor(146, 'r'),
                 Neighbor(138, 'p')],
            'd':[Neighbor(75, 'm'),
                 Neighbor(120, 'c')],
            'e':[Neighbor(86, 'h')],
            'f':[Neighbor(99, 's'),
                 Neighbor(211, 'b')],
            'g':[Neighbor(90, 'b')],
            'h':[Neighbor(98, 'u'),
                 Neighbor(86, 'e')],
            'i':[Neighbor(87, 'n'),
                 Neighbor(92, 'v')],
            'l':[Neighbor(111, 't'),
                 Neighbor(70, 'm')],
            'm':[Neighbor(70, 'l'),
                 Neighbor(75, 'd')],
            'n':[Neighbor(87, 'i')],
            'o':[Neighbor(151, 's'),
                 Neighbor(71, 'z')],
            'p':[Neighbor(97, 'r'),
                 Neighbor(101, 'b'),
                 Neighbor(138, 'c')],
            'r':[Neighbor(80, 's'),
                 Neighbor(97, 'p'),
                 Neighbor(147, 'c')],
            's':[Neighbor(151, 'o'),
                 Neighbor(99, 'f'),
                 Neighbor(80, 'r'),
                 Neighbor(140, 'a')],
            't':[Neighbor(118, 'a'),
                 Neighbor(111, 'l')],
            'u':[Neighbor(142, 'v'),
                 Neighbor(98, 'h'),
                 Neighbor(85, 'b')],
            'v':[Neighbor(92, 'i'),
                 Neighbor(142, 'u')],
            'z':[Neighbor(71, 'o'),
                 Neighbor(75, 'a')],
            }
        self.__heuristic = {
            'a':366,
            'b':0,
            'c':160,
            'd':242,
            'e':161,
            'f':176,
            'g':77,
            'h':151,
            'i':226,
            'l':244,
            'm':241,
            'n':234,
            'o':380,
            'p':100,
            'r':193,
            's':253,
            't':329,
            'u':80,
            'v':199,
            'z':374,
            }
        return

    def _heuristic (self, state, action):
        return self.__heuristic[action.gotoState]

    def _stepCost (self, state, action):
        cost = None
        for n in self.__neighbors[state]:
            if n.state == action.gotoState: cost = n.cost
            pass
        return cost
    
    def actions (self, state):
        result = []
        for n in self.__neighbors[state]: result.append (Action(n.state))
        return result

    def expand (self, node):
        path = "==> No path <=="
        
        if node is not None:
            path = self.__names[node.state]
            node = node.parent
            while node is not None:
                path = self.__names[node.state] + " --> " + path
                node = node.parent
                pass
            pass
        
        return path
    pass

def test (verbose=False):
    import search.general
    print "\n\nBreadth First Strategy\n======"
    problem = TravelMap(strategy=BreadthFirstStrategy())
    solution = search.general.find (problem, verbose)
    print "Solution: " + problem.expand (solution)
    print "\n\nUniform Cost Strategy\n======"
    h = TravelMap()
    problem = TravelMap(strategy=UniformCostStrategy(h._stepCost))
    solution = search.general.find (problem, verbose)
    print "Solution: " + problem.expand (solution)
    print "\n\nA* Strategy\n======"
    problem = TravelMap()
    solution = search.general.find (problem, verbose)
    print "Solution: " + problem.expand (solution)
    pass
