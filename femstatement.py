from enum import Enum

class Kind(Enum):
    dirichlet = 1
    neumann = 2
    robin = 3

class Condition:
    def __init__(self, kind, value):
        self.kind = None
        if kind == 'dirichlet':
            self.kind = Kind.dirichlet
        if kind == 'neumann':
            self.kind = Kind.neumann
        if kind == 'robin':
            self.kind = Kind.robin
        self.value = value

class FemStatement:
    def __init__(self, settings):
        self.origin = settings['limits']['start']
        self.end = settings['limits']['end']
        self.elemsNum = settings['elemsNum']
        self.m = settings['equation']['d2u']
        self.k = settings['equation']['du']
        self.c = settings['equation']['u']
        self.f = settings['equation']['rightSide']
        self.leftCond = Condition(settings['borderConditions']['left']['type'],
                                  settings['borderConditions']['left']['value'])
        self.rightCond = Condition(settings['borderConditions']['right']['type'],
                                   settings['borderConditions']['right']['value'])
    def nodesNum(self):
        return self.elemsNum + 1
    def elemLen(self):
        return self.len() / self.elemsNum
    def len(self):
        return self.end - self.origin

class FemCubicStatement(FemStatement):
    def nodesNum(self):
        return 3 * self.elemsNum + 1
    def subElemsLen(self):
        return self.elemLen() / 3.0