from femstatement import FemStatement, Kind
from fem_common import *
from slae import SLAE

def inner(p):
    """
    :type p: FemStatement
    """
    m = p.m
    k = p.k
    c = p.c
    f = p.f
    l = p.elemLen()
    locMx = allocateMx(2, 3)

    locMx[0][0] = -m/l - 0.5*k + c*l/3.0
    locMx[0][1] = m/l + 0.5*k + c*l/6.0
    locMx[0][2] = f*l*0.5

    locMx[1][0] = m/l - 0.5*k + c*l/6.0
    locMx[1][1] = -m/l + 0.5*k + c*l/3.0
    locMx[1][2] = f*l*0.5

    return locMx

def dirichletLeft(p):
    """
    :type p: FemStatement
    """
    m = p.m
    k = p.k
    c = p.c
    f = p.f
    l = p.elemLen()
    locMx = allocateMx(2, 3)

    locMx[0][0] = -m
    locMx[0][1] = m/l + 0.5*k + c*l/6.0
    locMx[0][2] = f*l*0.5 - p.leftCond.value*(-m/l - 0.5*k + c*l/3.0)

    locMx[1][0] = 0.0
    locMx[1][1] = -m/l + 0.5*k + c*l/3.0
    locMx[1][2] = f*l*0.5 - p.leftCond.value*(m/l - 0.5*k + c*l/6.0)

    return locMx

def dirichletRight(p):
    """
    :type p: FemStatement
    """
    m = p.m
    k = p.k
    c = p.c
    f = p.f
    l = p.elemLen()
    locMx = allocateMx(2, 3)

    locMx[0][0] = -m/l - 0.5*k + c*l/3.0
    locMx[0][1] = 0.0
    locMx[0][2] = f*l*0.5 - p.rightCond.value*(m/l + 0.5*k + c*l/6.0)

    locMx[1][0] = m/l - 0.5*k + c*l/6.0
    locMx[1][1] = m
    locMx[1][2] = f*l*0.5 - p.rightCond.value*(-m/l + 0.5*k + c*l/3.0)

    return locMx

def neumannLeft(p):
    """
    :type p: FemStatement
    """
    m = p.m
    k = p.k
    c = p.c
    f = p.f
    l = p.elemLen()
    locMx = allocateMx(2, 3)

    locMx[0][0] = -m/l - 0.5*k + c*l/3.0
    locMx[0][1] = m/l + 0.5*k + c*l/6.0
    locMx[0][2] = f*l*0.5 + m*p.leftCond.value

    locMx[1][0] = m/l - 0.5*k + c*l/6.0
    locMx[1][1] = -m/l + 0.5*k + c*l/3.0
    locMx[1][2] = f*l*0.5

    return locMx

def neumannRight(p):
    """
    :type p: FemStatement
    """
    m = p.m
    k = p.k
    c = p.c
    f = p.f
    l = p.elemLen()
    locMx = allocateMx(2, 3)

    locMx[0][0] = -m/l - 0.5*k + c*l/3.0
    locMx[0][1] = m/l + 0.5*k + c*l/6.0
    locMx[0][2] = f*l*0.5

    locMx[1][0] = m/l - 0.5*k + c*l/6.0
    locMx[1][1] = -m/l + 0.5*k + c*l/3.0
    locMx[1][2] = f*l*0.5 - m*p.rightCond.value

    return locMx

def robinLeft(p):
    """
    :type p: FemStatement
    """
    k1 = p.leftCond.value[0] / p.leftCond.value[1]
    k2 = p.leftCond.value[2] / p.leftCond.value[1]
    m = p.m
    k = p.k
    c = p.c
    f = p.f
    l = p.elemLen()
    locMx = allocateMx(2, 3)

    locMx[0][0] = -m/l - 0.5*k + c*l/3.0 + m*k1
    locMx[0][1] = m/l + 0.5*k + c*l/6.0
    locMx[0][2] = f*l*0.5 + m*k2

    locMx[1][0] = m/l - 0.5*k + c*l/6.0
    locMx[1][1] = -m/l + 0.5*k + c*l/3.0
    locMx[1][2] = f*l*0.5

    return locMx

def robinRight(p):
    """
    :type p: FemStatement
    """
    k1 = p.rightCond.value[0] / p.rightCond.value[1]    #Где-то здесь ошибка!
    k2 = p.rightCond.value[2] / p.rightCond.value[1]
    m = p.m
    k = p.k
    c = p.c
    f = p.f
    l = p.elemLen()
    locMx = allocateMx(2, 3)

    locMx[0][0] = -m/l - 0.5*k + c*l/3.0
    locMx[0][1] = m/l + 0.5*k + c*l/6.0
    locMx[0][2] = f*l*0.5

    locMx[1][0] = m/l - 0.5*k + c*l/6.0
    locMx[1][1] = -m/l + 0.5*k + c*l/3.0 - m*k1
    locMx[1][2] = f*l*0.5 - m*k2

    return locMx

def addToGlobal(glob, sz, local, e):
    d = 1
    for i in range(0, d+1):
        for j in range(0, d+1):
            glob[d*e+i][d*e+j] += local[i][j]
        glob[d*e+i][sz] += local[i][d+1]

def globalMx(p):
    """
    :type p: FemStatement
    """
    left = allocateMx(2, 3)
    right = allocateMx(2, 3)

    if p.leftCond.kind == Kind.dirichlet:
        left = dirichletLeft(p)
    elif p.leftCond.kind == Kind.neumann:
        left = neumannLeft(p)
    elif p.leftCond.kind == Kind.robin:
        left = robinLeft(p)

    if p.rightCond.kind == Kind.dirichlet:
        right = dirichletRight(p)
    elif p.rightCond.kind == Kind.neumann:
        right = neumannRight(p)
    elif p.rightCond.kind == Kind.robin:
        right = robinRight(p)

    inner_matrix = inner(p)

    mx = allocateMx(p.nodesNum(), p.nodesNum()+1)

    addToGlobal(mx, p.nodesNum(), left, 0)

    for e in range(1, p.elemsNum-1):
        addToGlobal(mx, p.nodesNum(), inner_matrix, e)

    addToGlobal(mx, p.nodesNum(), right, p.elemsNum-1)

    return mx

def driver(p):
    """
    :type p: FemStatement
    """
    sl = SLAE()
    sl.insertMatrix(globalMx(p), p.nodesNum())
    sl.solve()
    S = allocateMx(p.nodesNum(), 1)

    sl.copySoln(S)
    if p.leftCond.kind is Kind.dirichlet:
        S[0] = p.leftCond.value
    if p.rightCond.kind is Kind.dirichlet:
        S[p.nodesNum()-1] = p.rightCond.value

    results = allocateMx(p.nodesNum(), 2)
    for i in range(0, p.nodesNum()):
        results[i][0] = p.origin + p.elemLen()*i
        results[i][1] = S[i]

    return results